from netbox.graphql.types import NetBoxObjectType

from .. import filtersets, models


class ProviderType(NetBoxObjectType):
    class Meta:
        model = models.Provider
        fields = "__all__"
        filterset_class = filtersets.ProviderFilterSet


class ContractType(NetBoxObjectType):
    class Meta:
        model = models.Contract
        fields = "__all__"
        filterset_class = filtersets.ContractFilterSet


class HardwareNoticeType(NetBoxObjectType):
    class Meta:
        model = models.HardwareNotice
        fields = "__all__"
        filterset_class = filtersets.HardwareNoticeFilterSet


class SoftwareVersionType(NetBoxObjectType):
    class Meta:
        model = models.SoftwareVersion
        fields = "__all__"
        filterset_class = filtersets.SoftwareVersionFilterSet


class SoftwareImageFileType(NetBoxObjectType):
    class Meta:
        model = models.SoftwareImageFile
        fields = "__all__"
        filterset_class = filtersets.SoftwareImageFileFilterSet


class DeviceSoftwareType(NetBoxObjectType):
    class Meta:
        model = models.DeviceSoftware
        fields = "__all__"
        filterset_class = filtersets.DeviceSoftwareFilterSet


class ValidatedSoftwareType(NetBoxObjectType):
    class Meta:
        model = models.ValidatedSoftware
        fields = "__all__"
        filterset_class = filtersets.ValidatedSoftwareFilterSet


class CVEType(NetBoxObjectType):
    class Meta:
        model = models.CVE
        fields = "__all__"
        filterset_class = filtersets.CVEFilterSet


class VulnerabilityType(NetBoxObjectType):
    class Meta:
        model = models.Vulnerability
        fields = "__all__"
        filterset_class = filtersets.VulnerabilityFilterSet
