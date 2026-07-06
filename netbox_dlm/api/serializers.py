from dcim.api.serializers import (
    DeviceSerializer,
    DeviceRoleSerializer,
    DeviceTypeSerializer,
    ModuleTypeSerializer,
    PlatformSerializer,
)
from netbox.api.fields import ChoiceField
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ..choices import (
    ContractSupportLevelChoices,
    CVESeverityChoices,
    CVEStatusChoices,
    HashingAlgorithmChoices,
    VulnerabilityStatusChoices,
)
from ..models import (
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


class ProviderSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dlm-api:provider-detail"
    )

    class Meta:
        model = Provider
        fields = (
            "id", "url", "display", "name", "physical_address", "phone",
            "email", "portal_url", "comments", "tags", "custom_fields",
            "created", "last_updated",
        )


class ContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dlm-api:contract-detail"
    )
    provider = ProviderSerializer(nested=True)
    support_level = ChoiceField(choices=ContractSupportLevelChoices, required=False)
    devices = DeviceSerializer(nested=True, many=True, required=False)

    class Meta:
        model = Contract
        fields = (
            "id", "url", "display", "provider", "name", "contract_number",
            "start_date", "end_date", "cost", "currency", "support_level",
            "devices", "comments", "tags", "custom_fields", "created", "last_updated",
        )


class HardwareNoticeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dlm-api:hardwarenotice-detail"
    )
    device_type = DeviceTypeSerializer(nested=True, required=False, allow_null=True)
    module_type = ModuleTypeSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = HardwareNotice
        fields = (
            "id", "url", "display", "device_type", "module_type", "end_of_sale",
            "end_of_support", "end_of_security_patches", "end_of_sw_releases",
            "documentation_url", "comments", "tags", "custom_fields",
            "created", "last_updated",
        )


class SoftwareVersionSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dlm-api:softwareversion-detail"
    )
    platform = PlatformSerializer(nested=True)

    class Meta:
        model = SoftwareVersion
        fields = (
            "id", "url", "display", "platform", "version", "alias",
            "release_date", "end_of_support", "long_term_support",
            "documentation_url", "comments", "tags", "custom_fields",
            "created", "last_updated",
        )


class SoftwareImageFileSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dlm-api:softwareimagefile-detail"
    )
    software_version = SoftwareVersionSerializer(nested=True)
    hashing_algorithm = ChoiceField(choices=HashingAlgorithmChoices, required=False)

    class Meta:
        model = SoftwareImageFile
        fields = (
            "id", "url", "display", "software_version", "file_name", "checksum",
            "hashing_algorithm", "file_size", "download_url", "default_image",
            "comments", "tags", "custom_fields", "created", "last_updated",
        )


class DeviceSoftwareSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dlm-api:devicesoftware-detail"
    )
    device = DeviceSerializer(nested=True)
    software_version = SoftwareVersionSerializer(nested=True)

    class Meta:
        model = DeviceSoftware
        fields = (
            "id", "url", "display", "device", "software_version", "last_checked",
            "comments", "tags", "custom_fields", "created", "last_updated",
        )


class ValidatedSoftwareSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dlm-api:validatedsoftware-detail"
    )
    software_version = SoftwareVersionSerializer(nested=True)
    device_types = DeviceTypeSerializer(nested=True, many=True, required=False)
    device_roles = DeviceRoleSerializer(nested=True, many=True, required=False)
    devices = DeviceSerializer(nested=True, many=True, required=False)

    class Meta:
        model = ValidatedSoftware
        fields = (
            "id", "url", "display", "software_version", "device_types",
            "device_roles", "devices", "start", "end", "preferred",
            "comments", "tags", "custom_fields", "created", "last_updated",
        )


class CVESerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dlm-api:cve-detail"
    )
    status = ChoiceField(choices=CVEStatusChoices, required=False)
    severity = ChoiceField(choices=CVESeverityChoices, required=False)
    affected_software = SoftwareVersionSerializer(nested=True, many=True, required=False)

    class Meta:
        model = CVE
        fields = (
            "id", "url", "display", "cve_id", "name", "description",
            "published_date", "link", "status", "severity", "cvss_score",
            "cvss_v2_score", "cvss_v3_score", "affected_software", "comments",
            "tags", "custom_fields", "created", "last_updated",
        )


class VulnerabilitySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dlm-api:vulnerability-detail"
    )
    cve = CVESerializer(nested=True)
    software_version = SoftwareVersionSerializer(nested=True)
    device = DeviceSerializer(nested=True, required=False, allow_null=True)
    status = ChoiceField(choices=VulnerabilityStatusChoices, required=False)

    class Meta:
        model = Vulnerability
        fields = (
            "id", "url", "display", "cve", "software_version", "device",
            "status", "comments", "tags", "custom_fields", "created", "last_updated",
        )
