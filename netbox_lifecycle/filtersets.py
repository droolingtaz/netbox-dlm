import django_filters
from django.db.models import Q

from dcim.models import Device, DeviceRole, DeviceType, ModuleType, Platform
from netbox.filtersets import NetBoxModelFilterSet

from .choices import (
    ContractSupportLevelChoices,
    CVESeverityChoices,
    CVEStatusChoices,
    VulnerabilityStatusChoices,
)
from .models import (
    CVE,
    Contract,
    DeviceSoftware,
    HardwareNotice,
    Provider,
    SoftwareImageFile,
    SoftwareVersion,
    ValidatedSoftware,
    Vulnerability,
)


class ProviderFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Provider
        fields = ("id", "name", "phone", "email")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(email__icontains=value) | Q(phone__icontains=value)
        )


class ContractFilterSet(NetBoxModelFilterSet):
    provider_id = django_filters.ModelMultipleChoiceFilter(queryset=Provider.objects.all())
    support_level = django_filters.MultipleChoiceFilter(choices=ContractSupportLevelChoices)
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name="devices", queryset=Device.objects.all()
    )

    class Meta:
        model = Contract
        fields = ("id", "name", "contract_number", "provider_id", "support_level")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(contract_number__icontains=value))


class HardwareNoticeFilterSet(NetBoxModelFilterSet):
    device_type_id = django_filters.ModelMultipleChoiceFilter(queryset=DeviceType.objects.all())
    module_type_id = django_filters.ModelMultipleChoiceFilter(queryset=ModuleType.objects.all())

    class Meta:
        model = HardwareNotice
        fields = ("id", "device_type_id", "module_type_id")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(device_type__model__icontains=value) | Q(module_type__model__icontains=value)
        )


class SoftwareVersionFilterSet(NetBoxModelFilterSet):
    platform_id = django_filters.ModelMultipleChoiceFilter(queryset=Platform.objects.all())
    long_term_support = django_filters.BooleanFilter()

    class Meta:
        model = SoftwareVersion
        fields = ("id", "platform_id", "version", "long_term_support")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(version__icontains=value) | Q(alias__icontains=value))


class SoftwareImageFileFilterSet(NetBoxModelFilterSet):
    software_version_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SoftwareVersion.objects.all()
    )

    class Meta:
        model = SoftwareImageFile
        fields = ("id", "software_version_id", "file_name", "default_image")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(file_name__icontains=value) | Q(checksum__icontains=value))


class DeviceSoftwareFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(queryset=Device.objects.all())
    software_version_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SoftwareVersion.objects.all()
    )

    class Meta:
        model = DeviceSoftware
        fields = ("id", "device_id", "software_version_id")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(device__name__icontains=value))


class ValidatedSoftwareFilterSet(NetBoxModelFilterSet):
    software_version_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SoftwareVersion.objects.all()
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device_types", queryset=DeviceType.objects.all()
    )
    device_role_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device_roles", queryset=DeviceRole.objects.all()
    )
    preferred = django_filters.BooleanFilter()

    class Meta:
        model = ValidatedSoftware
        fields = ("id", "software_version_id", "preferred")

    def search(self, queryset, name, value):
        return queryset


class CVEFilterSet(NetBoxModelFilterSet):
    severity = django_filters.MultipleChoiceFilter(choices=CVESeverityChoices)
    status = django_filters.MultipleChoiceFilter(choices=CVEStatusChoices)
    affected_software_id = django_filters.ModelMultipleChoiceFilter(
        field_name="affected_software", queryset=SoftwareVersion.objects.all()
    )

    class Meta:
        model = CVE
        fields = ("id", "cve_id", "severity", "status")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(cve_id__icontains=value) | Q(name__icontains=value) | Q(description__icontains=value)
        )


class VulnerabilityFilterSet(NetBoxModelFilterSet):
    cve_id = django_filters.ModelMultipleChoiceFilter(queryset=CVE.objects.all())
    device_id = django_filters.ModelMultipleChoiceFilter(queryset=Device.objects.all())
    software_version_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SoftwareVersion.objects.all()
    )
    status = django_filters.MultipleChoiceFilter(choices=VulnerabilityStatusChoices)

    class Meta:
        model = Vulnerability
        fields = ("id", "cve_id", "device_id", "software_version_id", "status")

    def search(self, queryset, name, value):
        return queryset
