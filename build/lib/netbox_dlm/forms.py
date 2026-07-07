from django import forms

from dcim.models import Device, DeviceRole, DeviceType, ModuleType, Platform
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

from .choices import (
    ContractSupportLevelChoices,
    CVESeverityChoices,
    CVEStatusChoices,
    HashingAlgorithmChoices,
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


# -----------------------------------------------------------------------------
# Provider / Contract
# -----------------------------------------------------------------------------

class ProviderForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = Provider
        fields = ("name", "physical_address", "phone", "email", "portal_url", "comments", "tags")


class ContractForm(NetBoxModelForm):
    provider = DynamicModelChoiceField(queryset=Provider.objects.all())
    devices = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False)
    comments = CommentField()

    fieldsets = (
        FieldSet("provider", "name", "contract_number", "support_level", name="Contract"),
        FieldSet("start_date", "end_date", "cost", "currency", name="Term"),
        FieldSet("devices", name="Coverage"),
    )

    class Meta:
        model = Contract
        fields = (
            "provider", "name", "contract_number", "support_level", "start_date",
            "end_date", "cost", "currency", "devices", "comments", "tags",
        )
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ContractFilterForm(NetBoxModelFilterSetForm):
    model = Contract
    provider_id = DynamicModelMultipleChoiceField(queryset=Provider.objects.all(), required=False)
    support_level = forms.MultipleChoiceField(choices=ContractSupportLevelChoices, required=False)
    device_id = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False)


# -----------------------------------------------------------------------------
# Hardware notices
# -----------------------------------------------------------------------------

class HardwareNoticeForm(NetBoxModelForm):
    device_type = DynamicModelChoiceField(queryset=DeviceType.objects.all(), required=False)
    module_type = DynamicModelChoiceField(queryset=ModuleType.objects.all(), required=False)
    comments = CommentField()

    fieldsets = (
        FieldSet("device_type", "module_type", name="Hardware"),
        FieldSet(
            "end_of_sale", "end_of_support", "end_of_security_patches",
            "end_of_sw_releases", "documentation_url", name="Dates",
        ),
    )

    class Meta:
        model = HardwareNotice
        fields = (
            "device_type", "module_type", "end_of_sale", "end_of_support",
            "end_of_security_patches", "end_of_sw_releases", "documentation_url",
            "comments", "tags",
        )
        widgets = {
            "end_of_sale": forms.DateInput(attrs={"type": "date"}),
            "end_of_support": forms.DateInput(attrs={"type": "date"}),
            "end_of_security_patches": forms.DateInput(attrs={"type": "date"}),
            "end_of_sw_releases": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        device_type = cleaned_data.get("device_type")
        module_type = cleaned_data.get("module_type")
        if bool(device_type) == bool(module_type):
            raise forms.ValidationError(
                "Select exactly one of device type or module type."
            )
        return cleaned_data


class HardwareNoticeFilterForm(NetBoxModelFilterSetForm):
    model = HardwareNotice
    device_type_id = DynamicModelMultipleChoiceField(queryset=DeviceType.objects.all(), required=False)
    module_type_id = DynamicModelMultipleChoiceField(queryset=ModuleType.objects.all(), required=False)


# -----------------------------------------------------------------------------
# Software
# -----------------------------------------------------------------------------

class SoftwareVersionForm(NetBoxModelForm):
    platform = DynamicModelChoiceField(queryset=Platform.objects.all())
    comments = CommentField()

    class Meta:
        model = SoftwareVersion
        fields = (
            "platform", "version", "alias", "release_date", "end_of_support",
            "long_term_support", "documentation_url", "comments", "tags",
        )
        widgets = {
            "release_date": forms.DateInput(attrs={"type": "date"}),
            "end_of_support": forms.DateInput(attrs={"type": "date"}),
        }


class SoftwareVersionFilterForm(NetBoxModelFilterSetForm):
    model = SoftwareVersion
    platform_id = DynamicModelMultipleChoiceField(queryset=Platform.objects.all(), required=False)
    long_term_support = forms.NullBooleanField(
        required=False, widget=forms.Select(choices=[("", "---"), ("true", "Yes"), ("false", "No")])
    )


class SoftwareImageFileForm(NetBoxModelForm):
    software_version = DynamicModelChoiceField(queryset=SoftwareVersion.objects.all())
    comments = CommentField()

    class Meta:
        model = SoftwareImageFile
        fields = (
            "software_version", "file_name", "checksum", "hashing_algorithm",
            "file_size", "download_url", "default_image", "comments", "tags",
        )


class SoftwareImageFileFilterForm(NetBoxModelFilterSetForm):
    model = SoftwareImageFile
    software_version_id = DynamicModelMultipleChoiceField(
        queryset=SoftwareVersion.objects.all(), required=False
    )


class DeviceSoftwareForm(NetBoxModelForm):
    device = DynamicModelChoiceField(queryset=Device.objects.all())
    software_version = DynamicModelChoiceField(queryset=SoftwareVersion.objects.all())
    comments = CommentField()

    class Meta:
        model = DeviceSoftware
        fields = ("device", "software_version", "last_checked", "comments", "tags")
        widgets = {
            "last_checked": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class DeviceSoftwareFilterForm(NetBoxModelFilterSetForm):
    model = DeviceSoftware
    device_id = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False)
    software_version_id = DynamicModelMultipleChoiceField(
        queryset=SoftwareVersion.objects.all(), required=False
    )


class ValidatedSoftwareForm(NetBoxModelForm):
    software_version = DynamicModelChoiceField(queryset=SoftwareVersion.objects.all())
    device_types = DynamicModelMultipleChoiceField(queryset=DeviceType.objects.all(), required=False)
    device_roles = DynamicModelMultipleChoiceField(queryset=DeviceRole.objects.all(), required=False)
    devices = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False)
    comments = CommentField()

    fieldsets = (
        FieldSet("software_version", "start", "end", "preferred", name="Rule"),
        FieldSet("device_types", "device_roles", "devices", name="Scope"),
    )

    class Meta:
        model = ValidatedSoftware
        fields = (
            "software_version", "device_types", "device_roles", "devices",
            "start", "end", "preferred", "comments", "tags",
        )
        widgets = {
            "start": forms.DateInput(attrs={"type": "date"}),
            "end": forms.DateInput(attrs={"type": "date"}),
        }


class ValidatedSoftwareFilterForm(NetBoxModelFilterSetForm):
    model = ValidatedSoftware
    software_version_id = DynamicModelMultipleChoiceField(
        queryset=SoftwareVersion.objects.all(), required=False
    )
    device_type_id = DynamicModelMultipleChoiceField(queryset=DeviceType.objects.all(), required=False)
    device_role_id = DynamicModelMultipleChoiceField(queryset=DeviceRole.objects.all(), required=False)
    preferred = forms.NullBooleanField(
        required=False, widget=forms.Select(choices=[("", "---"), ("true", "Yes"), ("false", "No")])
    )


# -----------------------------------------------------------------------------
# CVE / Vulnerability
# -----------------------------------------------------------------------------

class CVEForm(NetBoxModelForm):
    affected_software = DynamicModelMultipleChoiceField(
        queryset=SoftwareVersion.objects.all(), required=False
    )
    comments = CommentField()

    class Meta:
        model = CVE
        fields = (
            "cve_id", "name", "description", "published_date", "link", "status",
            "severity", "cvss_score", "cvss_v2_score", "cvss_v3_score",
            "affected_software", "comments", "tags",
        )
        widgets = {
            "published_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class CVEFilterForm(NetBoxModelFilterSetForm):
    model = CVE
    severity = forms.MultipleChoiceField(choices=CVESeverityChoices, required=False)
    status = forms.MultipleChoiceField(choices=CVEStatusChoices, required=False)
    affected_software_id = DynamicModelMultipleChoiceField(
        queryset=SoftwareVersion.objects.all(), required=False
    )


class VulnerabilityForm(NetBoxModelForm):
    cve = DynamicModelChoiceField(queryset=CVE.objects.all())
    software_version = DynamicModelChoiceField(queryset=SoftwareVersion.objects.all())
    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    comments = CommentField()

    class Meta:
        model = Vulnerability
        fields = ("cve", "software_version", "device", "status", "comments", "tags")


class VulnerabilityFilterForm(NetBoxModelFilterSetForm):
    model = Vulnerability
    cve_id = DynamicModelMultipleChoiceField(queryset=CVE.objects.all(), required=False)
    device_id = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False)
    software_version_id = DynamicModelMultipleChoiceField(
        queryset=SoftwareVersion.objects.all(), required=False
    )
    status = forms.MultipleChoiceField(choices=VulnerabilityStatusChoices, required=False)
