from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets
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
from . import serializers


class ProviderViewSet(NetBoxModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = serializers.ProviderSerializer
    filterset_class = filtersets.ProviderFilterSet


class ContractViewSet(NetBoxModelViewSet):
    queryset = Contract.objects.prefetch_related("provider", "devices", "tags")
    serializer_class = serializers.ContractSerializer
    filterset_class = filtersets.ContractFilterSet


class HardwareNoticeViewSet(NetBoxModelViewSet):
    queryset = HardwareNotice.objects.prefetch_related("device_type", "module_type", "tags")
    serializer_class = serializers.HardwareNoticeSerializer
    filterset_class = filtersets.HardwareNoticeFilterSet


class SoftwareVersionViewSet(NetBoxModelViewSet):
    queryset = SoftwareVersion.objects.prefetch_related("platform", "tags")
    serializer_class = serializers.SoftwareVersionSerializer
    filterset_class = filtersets.SoftwareVersionFilterSet


class SoftwareImageFileViewSet(NetBoxModelViewSet):
    queryset = SoftwareImageFile.objects.prefetch_related("software_version", "tags")
    serializer_class = serializers.SoftwareImageFileSerializer
    filterset_class = filtersets.SoftwareImageFileFilterSet


class DeviceSoftwareViewSet(NetBoxModelViewSet):
    queryset = DeviceSoftware.objects.prefetch_related("device", "software_version", "tags")
    serializer_class = serializers.DeviceSoftwareSerializer
    filterset_class = filtersets.DeviceSoftwareFilterSet


class ValidatedSoftwareViewSet(NetBoxModelViewSet):
    queryset = ValidatedSoftware.objects.prefetch_related(
        "software_version", "device_types", "device_roles", "devices", "tags"
    )
    serializer_class = serializers.ValidatedSoftwareSerializer
    filterset_class = filtersets.ValidatedSoftwareFilterSet


class CVEViewSet(NetBoxModelViewSet):
    queryset = CVE.objects.prefetch_related("affected_software", "tags")
    serializer_class = serializers.CVESerializer
    filterset_class = filtersets.CVEFilterSet


class VulnerabilityViewSet(NetBoxModelViewSet):
    queryset = Vulnerability.objects.prefetch_related("cve", "software_version", "device", "tags")
    serializer_class = serializers.VulnerabilitySerializer
    filterset_class = filtersets.VulnerabilityFilterSet
