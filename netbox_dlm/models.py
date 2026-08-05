import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from dcim.models import (
    Device,
    DeviceRole,
    DeviceType,
    InventoryItem,
    InventoryItemRole,
    ModuleType,
    Platform,
)
from netbox.models import NetBoxModel

from .choices import (
    ContractSupportLevelChoices,
    CVESeverityChoices,
    CVEStatusChoices,
    HashingAlgorithmChoices,
    ReleaseDesignationChoices,
    VulnerabilityStatusChoices,
)


# -----------------------------------------------------------------------------
# Contracts
# -----------------------------------------------------------------------------

class Provider(NetBoxModel):
    """A vendor, reseller, or support organization behind a maintenance contract."""

    name = models.CharField(max_length=100, unique=True)
    physical_address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    portal_url = models.URLField(blank=True, verbose_name="Support portal URL")
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:provider", args=[self.pk])


class Contract(NetBoxModel):
    """A maintenance/support contract covering one or more devices."""

    provider = models.ForeignKey(
        to=Provider, on_delete=models.PROTECT, related_name="contracts"
    )
    name = models.CharField(max_length=100)
    contract_number = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, default="USD", blank=True)
    support_level = models.CharField(
        max_length=30, choices=ContractSupportLevelChoices, blank=True
    )
    devices = models.ManyToManyField(
        to=Device, related_name="lifecycle_contracts", blank=True
    )
    platforms = models.ManyToManyField(to=Platform, related_name="+", blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("provider", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("provider", "name"), name="%(app_label)s_%(class)s_unique_provider_name"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.provider})"

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:contract", args=[self.pk])

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date must be on or after the start date."})

    @property
    def expired(self):
        return bool(self.end_date and self.end_date < timezone.localdate())

    @property
    def expiring_soon(self, days=90):
        if not self.end_date:
            return False
        return timezone.localdate() <= self.end_date <= timezone.localdate() + datetime.timedelta(days=days)

    def covers_device(self, device):
        """
        Whether this contract covers the given device, either because it's
        explicitly listed or because its platform is covered. Unlike
        ValidatedSoftware, an empty scope covers nothing — a support
        contract shouldn't silently apply to every device just because
        nobody scoped it yet.
        """
        if self.devices.filter(pk=device.pk).exists():
            return True
        return bool(device.platform_id and self.platforms.filter(pk=device.platform_id).exists())

    @property
    def covered_devices(self):
        """All devices covered by this contract: explicit devices plus any
        whose platform is in scope."""
        return Device.objects.filter(
            models.Q(lifecycle_contracts=self) | models.Q(platform__in=self.platforms.all())
        ).distinct()


# -----------------------------------------------------------------------------
# Hardware lifecycle
# -----------------------------------------------------------------------------

class HardwareNotice(NetBoxModel):
    """
    End-of-life / end-of-support notice for a DeviceType or ModuleType.
    Exactly one of device_type / module_type must be set.
    """

    device_type = models.ForeignKey(
        to=DeviceType,
        on_delete=models.CASCADE,
        related_name="hardware_notices",
        blank=True,
        null=True,
    )
    module_type = models.ForeignKey(
        to=ModuleType,
        on_delete=models.CASCADE,
        related_name="hardware_notices",
        blank=True,
        null=True,
    )
    end_of_sale = models.DateField(blank=True, null=True)
    end_of_support = models.DateField(
        blank=True, null=True, verbose_name="End of support (last day of life)"
    )
    end_of_security_patches = models.DateField(blank=True, null=True)
    end_of_sw_releases = models.DateField(blank=True, null=True)
    documentation_url = models.URLField(blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("end_of_support", "device_type", "module_type")
        constraints = [
            models.UniqueConstraint(
                fields=("device_type",),
                condition=models.Q(device_type__isnull=False),
                name="%(app_label)s_%(class)s_unique_device_type",
            ),
            models.UniqueConstraint(
                fields=("module_type",),
                condition=models.Q(module_type__isnull=False),
                name="%(app_label)s_%(class)s_unique_module_type",
            ),
        ]

    def __str__(self):
        target = self.device_type or self.module_type
        return f"Hardware notice: {target}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:hardwarenotice", args=[self.pk])

    def clean(self):
        super().clean()
        if bool(self.device_type) == bool(self.module_type):
            raise ValidationError(
                "A hardware notice must reference exactly one of device type or module type."
            )

    @property
    def target(self):
        return self.device_type or self.module_type

    @property
    def end_of_support_passed(self):
        return bool(self.end_of_support and self.end_of_support < timezone.localdate())


# -----------------------------------------------------------------------------
# Software
# -----------------------------------------------------------------------------

class SoftwareVersion(NetBoxModel):
    """A specific software/firmware release for a Platform."""

    platform = models.ForeignKey(
        to=Platform, on_delete=models.CASCADE, related_name="software_versions"
    )
    version = models.CharField(max_length=50)
    alias = models.CharField(max_length=100, blank=True, help_text="Friendly display name")
    release_date = models.DateField(blank=True, null=True)
    end_of_support = models.DateField(blank=True, null=True, verbose_name="End of software support")
    long_term_support = models.BooleanField(default=False, verbose_name="LTS")
    release_designation = models.CharField(
        max_length=10,
        choices=ReleaseDesignationChoices,
        blank=True,
        verbose_name="Release designation",
        help_text=(
            "This version's position in the platform's release train. "
            "At most one version per platform may hold a given designation."
        ),
    )
    documentation_url = models.URLField(blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("platform", "version")
        constraints = [
            models.UniqueConstraint(
                fields=("platform", "version"), name="%(app_label)s_%(class)s_unique_platform_version"
            ),
            models.UniqueConstraint(
                fields=("platform", "release_designation"),
                condition=~models.Q(release_designation=""),
                name="%(app_label)s_%(class)s_unique_platform_release_designation",
            ),
        ]

    def __str__(self):
        return self.alias or f"{self.platform} {self.version}"

    @property
    def display(self):
        return str(self)

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:softwareversion", args=[self.pk])

    def get_release_designation_color(self):
        return ReleaseDesignationChoices.colors.get(self.release_designation)

    @property
    def end_of_support_passed(self):
        return bool(self.end_of_support and self.end_of_support < timezone.localdate())


class SoftwareImageFile(NetBoxModel):
    """A distributable image/file associated with a SoftwareVersion."""

    software_version = models.ForeignKey(
        to=SoftwareVersion, on_delete=models.CASCADE, related_name="image_files"
    )
    file_name = models.CharField(max_length=255)
    checksum = models.CharField(max_length=255, blank=True)
    hashing_algorithm = models.CharField(
        max_length=20, choices=HashingAlgorithmChoices, blank=True
    )
    file_size = models.BigIntegerField(blank=True, null=True, help_text="Size in bytes")
    download_url = models.URLField(blank=True)
    default_image = models.BooleanField(default=False)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("software_version", "file_name")
        constraints = [
            models.UniqueConstraint(
                fields=("software_version", "file_name"),
                name="%(app_label)s_%(class)s_unique_version_filename",
            )
        ]

    def __str__(self):
        return self.file_name

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:softwareimagefile", args=[self.pk])


class DeviceSoftware(NetBoxModel):
    """Tracks which SoftwareVersion is currently running on a given Device."""

    device = models.OneToOneField(
        to=Device, on_delete=models.CASCADE, related_name="lifecycle_software"
    )
    software_version = models.ForeignKey(
        to=SoftwareVersion, on_delete=models.PROTECT, related_name="devices_running"
    )
    last_checked = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("device",)
        verbose_name = "Device software"
        verbose_name_plural = "Device software"

    def __str__(self):
        return f"{self.device}: {self.software_version}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:devicesoftware", args=[self.pk])


class InventoryItemRolePlatform(NetBoxModel):
    """
    Declares which Platform's SoftwareVersions apply to InventoryItems of a
    given InventoryItemRole (e.g. "Management Controller" -> "Cisco CIMC").

    InventoryItem has no platform field of its own, unlike Device, so this
    mapping is what lets InventoryItemSoftware narrow/validate its
    SoftwareVersion choice the same way DeviceSoftware can rely on
    device.platform.
    """

    role = models.OneToOneField(
        to=InventoryItemRole, on_delete=models.CASCADE, related_name="lifecycle_platform"
    )
    platform = models.ForeignKey(
        to=Platform, on_delete=models.PROTECT, related_name="+"
    )
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("role",)
        verbose_name = "Inventory item role platform"
        verbose_name_plural = "Inventory item role platforms"

    def __str__(self):
        return f"{self.role} → {self.platform}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:inventoryitemroleplatform", args=[self.pk])


class InventoryItemSoftware(NetBoxModel):
    """Tracks which SoftwareVersion is currently running on a given InventoryItem."""

    inventory_item = models.OneToOneField(
        to=InventoryItem, on_delete=models.CASCADE, related_name="lifecycle_software"
    )
    software_version = models.ForeignKey(
        to=SoftwareVersion, on_delete=models.PROTECT, related_name="inventory_items_running"
    )
    last_checked = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("inventory_item",)
        verbose_name = "Inventory item software"
        verbose_name_plural = "Inventory item software"

    def __str__(self):
        return f"{self.inventory_item}: {self.software_version}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:inventoryitemsoftware", args=[self.pk])

    def clean(self):
        super().clean()
        if not (self.inventory_item_id and self.software_version_id):
            return
        role_id = self.inventory_item.role_id
        if not role_id:
            return
        mapping = InventoryItemRolePlatform.objects.filter(role_id=role_id).first()
        if mapping and self.software_version.platform_id != mapping.platform_id:
            raise ValidationError(
                {
                    "software_version": (
                        f"{self.inventory_item.role} inventory items require software "
                        f"from the {mapping.platform} platform."
                    )
                }
            )


class ValidatedSoftware(NetBoxModel):
    """
    An organizationally-approved software rule: this SoftwareVersion is valid
    for the given scope (device types / roles / specific devices / platforms /
    inventory item roles) during the given date range.
    """

    software_version = models.ForeignKey(
        to=SoftwareVersion, on_delete=models.CASCADE, related_name="validated_rules"
    )
    device_types = models.ManyToManyField(to=DeviceType, related_name="+", blank=True)
    device_roles = models.ManyToManyField(to=DeviceRole, related_name="+", blank=True)
    devices = models.ManyToManyField(to=Device, related_name="+", blank=True)
    platforms = models.ManyToManyField(to=Platform, related_name="+", blank=True)
    inventory_item_roles = models.ManyToManyField(
        to=InventoryItemRole, related_name="+", blank=True
    )
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    preferred = models.BooleanField(
        default=False,
        help_text="When multiple valid rules apply, the preferred one is used for compliance checks.",
    )
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("-preferred", "software_version", "start")
        verbose_name_plural = "Validated software"

    def __str__(self):
        return f"Validated: {self.software_version}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:validatedsoftware", args=[self.pk])

    def clean(self):
        super().clean()
        if self.end and self.end < self.start:
            raise ValidationError({"end": "End date must be on or after the start date."})

    @property
    def valid_now(self):
        today = timezone.localdate()
        if self.start > today:
            return False
        if self.end and self.end < today:
            return False
        return True

    def covers_device(self, device):
        """Whether this rule's scope includes the given device."""
        if self.devices.filter(pk=device.pk).exists():
            return True
        if self.device_types.filter(pk=device.device_type_id).exists():
            return True
        if device.role_id and self.device_roles.filter(pk=device.role_id).exists():
            return True
        if device.platform_id and self.platforms.filter(pk=device.platform_id).exists():
            return True
        # A rule with no scope at all applies to every device running that software.
        return not (
            self.devices.exists()
            or self.device_types.exists()
            or self.device_roles.exists()
            or self.platforms.exists()
            or self.inventory_item_roles.exists()
        )

    def covers_inventory_item(self, item):
        """Whether this rule's scope includes the given InventoryItem."""
        if item.role_id and self.inventory_item_roles.filter(pk=item.role_id).exists():
            return True
        if item.role_id:
            mapping = InventoryItemRolePlatform.objects.filter(role_id=item.role_id).first()
            if mapping and self.platforms.filter(pk=mapping.platform_id).exists():
                return True
        # A rule with no scope at all applies to every inventory item running that software.
        return not (
            self.devices.exists()
            or self.device_types.exists()
            or self.device_roles.exists()
            or self.platforms.exists()
            or self.inventory_item_roles.exists()
        )


# -----------------------------------------------------------------------------
# CVE / Vulnerability
# -----------------------------------------------------------------------------

class CVE(NetBoxModel):
    """A CVE record, generally populated from the NIST NVD API."""

    cve_id = models.CharField(max_length=20, unique=True, verbose_name="CVE ID")
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    published_date = models.DateField(blank=True, null=True)
    link = models.URLField(blank=True)
    status = models.CharField(
        max_length=30, choices=CVEStatusChoices, default=CVEStatusChoices.AWAITING_REVIEW
    )
    severity = models.CharField(max_length=10, choices=CVESeverityChoices, blank=True)
    cvss_score = models.FloatField(blank=True, null=True, verbose_name="CVSS score")
    cvss_v2_score = models.FloatField(blank=True, null=True, verbose_name="CVSSv2 score")
    cvss_v3_score = models.FloatField(blank=True, null=True, verbose_name="CVSSv3 score")
    affected_software = models.ManyToManyField(
        to=SoftwareVersion, related_name="cves", blank=True
    )
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("-published_date", "cve_id")
        verbose_name = "CVE"
        verbose_name_plural = "CVEs"

    def __str__(self):
        return self.cve_id

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:cve", args=[self.pk])


class Vulnerability(NetBoxModel):
    """
    A specific instance of exposure: a CVE affecting a SoftwareVersion,
    optionally scoped down to a single Device or InventoryItem.
    """

    cve = models.ForeignKey(to=CVE, on_delete=models.CASCADE, related_name="vulnerabilities")
    software_version = models.ForeignKey(
        to=SoftwareVersion, on_delete=models.CASCADE, related_name="vulnerabilities"
    )
    device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
        related_name="vulnerabilities",
        blank=True,
        null=True,
    )
    inventory_item = models.ForeignKey(
        to=InventoryItem,
        on_delete=models.CASCADE,
        related_name="vulnerabilities",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20, choices=VulnerabilityStatusChoices, default=VulnerabilityStatusChoices.OPEN
    )
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("cve", "software_version", "device", "inventory_item")
        verbose_name_plural = "Vulnerabilities"
        constraints = [
            models.UniqueConstraint(
                fields=("cve", "software_version", "device", "inventory_item"),
                name="%(app_label)s_%(class)s_unique_cve_software_device",
            )
        ]

    def __str__(self):
        scope = self.device or self.inventory_item or self.software_version
        return f"{self.cve} @ {scope}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_dlm:vulnerability", args=[self.pk])

    def clean(self):
        super().clean()
        if self.device_id and self.inventory_item_id:
            raise ValidationError(
                "Set at most one of device or inventory item, not both."
            )
