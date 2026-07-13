from netbox.views import generic

from . import filtersets, forms, tables
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
# Provider
# -----------------------------------------------------------------------------

class ProviderListView(generic.ObjectListView):
    queryset = Provider.objects.all()
    table = tables.ProviderTable
    filterset = filtersets.ProviderFilterSet


class ProviderView(generic.ObjectView):
    queryset = Provider.objects.all()


class ProviderEditView(generic.ObjectEditView):
    queryset = Provider.objects.all()
    form = forms.ProviderForm


class ProviderDeleteView(generic.ObjectDeleteView):
    queryset = Provider.objects.all()


class ProviderBulkDeleteView(generic.BulkDeleteView):
    queryset = Provider.objects.all()
    table = tables.ProviderTable
    filterset = filtersets.ProviderFilterSet


# -----------------------------------------------------------------------------
# Contract
# -----------------------------------------------------------------------------

class ContractListView(generic.ObjectListView):
    queryset = Contract.objects.all()
    table = tables.ContractTable
    filterset = filtersets.ContractFilterSet
    filterset_form = forms.ContractFilterForm


class ContractView(generic.ObjectView):
    queryset = Contract.objects.all()


class ContractEditView(generic.ObjectEditView):
    queryset = Contract.objects.all()
    form = forms.ContractForm


class ContractDeleteView(generic.ObjectDeleteView):
    queryset = Contract.objects.all()


class ContractBulkDeleteView(generic.BulkDeleteView):
    queryset = Contract.objects.all()
    table = tables.ContractTable
    filterset = filtersets.ContractFilterSet


# -----------------------------------------------------------------------------
# HardwareNotice
# -----------------------------------------------------------------------------

class HardwareNoticeListView(generic.ObjectListView):
    queryset = HardwareNotice.objects.all()
    table = tables.HardwareNoticeTable
    filterset = filtersets.HardwareNoticeFilterSet
    filterset_form = forms.HardwareNoticeFilterForm


class HardwareNoticeView(generic.ObjectView):
    queryset = HardwareNotice.objects.all()


class HardwareNoticeEditView(generic.ObjectEditView):
    queryset = HardwareNotice.objects.all()
    form = forms.HardwareNoticeForm


class HardwareNoticeDeleteView(generic.ObjectDeleteView):
    queryset = HardwareNotice.objects.all()


class HardwareNoticeBulkDeleteView(generic.BulkDeleteView):
    queryset = HardwareNotice.objects.all()
    table = tables.HardwareNoticeTable
    filterset = filtersets.HardwareNoticeFilterSet


# -----------------------------------------------------------------------------
# SoftwareVersion
# -----------------------------------------------------------------------------

class SoftwareVersionListView(generic.ObjectListView):
    queryset = SoftwareVersion.objects.all()
    table = tables.SoftwareVersionTable
    filterset = filtersets.SoftwareVersionFilterSet
    filterset_form = forms.SoftwareVersionFilterForm


class SoftwareVersionView(generic.ObjectView):
    queryset = SoftwareVersion.objects.all()

    def get_extra_context(self, request, instance):
        return {
            "image_files": instance.image_files.all(),
            "validated_rules": instance.validated_rules.all(),
            "cves": instance.cves.all(),
            "devices_running": instance.devices_running.select_related("device"),
        }


class SoftwareVersionEditView(generic.ObjectEditView):
    queryset = SoftwareVersion.objects.all()
    form = forms.SoftwareVersionForm


class SoftwareVersionDeleteView(generic.ObjectDeleteView):
    queryset = SoftwareVersion.objects.all()


class SoftwareVersionBulkDeleteView(generic.BulkDeleteView):
    queryset = SoftwareVersion.objects.all()
    table = tables.SoftwareVersionTable
    filterset = filtersets.SoftwareVersionFilterSet


# -----------------------------------------------------------------------------
# SoftwareImageFile
# -----------------------------------------------------------------------------

class SoftwareImageFileListView(generic.ObjectListView):
    queryset = SoftwareImageFile.objects.all()
    table = tables.SoftwareImageFileTable
    filterset = filtersets.SoftwareImageFileFilterSet
    filterset_form = forms.SoftwareImageFileFilterForm


class SoftwareImageFileView(generic.ObjectView):
    queryset = SoftwareImageFile.objects.all()


class SoftwareImageFileEditView(generic.ObjectEditView):
    queryset = SoftwareImageFile.objects.all()
    form = forms.SoftwareImageFileForm


class SoftwareImageFileDeleteView(generic.ObjectDeleteView):
    queryset = SoftwareImageFile.objects.all()


class SoftwareImageFileBulkDeleteView(generic.BulkDeleteView):
    queryset = SoftwareImageFile.objects.all()
    table = tables.SoftwareImageFileTable
    filterset = filtersets.SoftwareImageFileFilterSet


# -----------------------------------------------------------------------------
# DeviceSoftware
# -----------------------------------------------------------------------------

class DeviceSoftwareListView(generic.ObjectListView):
    queryset = DeviceSoftware.objects.all()
    table = tables.DeviceSoftwareTable
    filterset = filtersets.DeviceSoftwareFilterSet
    filterset_form = forms.DeviceSoftwareFilterForm


class DeviceSoftwareView(generic.ObjectView):
    queryset = DeviceSoftware.objects.all()


class DeviceSoftwareEditView(generic.ObjectEditView):
    queryset = DeviceSoftware.objects.all()
    form = forms.DeviceSoftwareForm


class DeviceSoftwareDeleteView(generic.ObjectDeleteView):
    queryset = DeviceSoftware.objects.all()


class DeviceSoftwareBulkDeleteView(generic.BulkDeleteView):
    queryset = DeviceSoftware.objects.all()
    table = tables.DeviceSoftwareTable
    filterset = filtersets.DeviceSoftwareFilterSet


# -----------------------------------------------------------------------------
# ValidatedSoftware
# -----------------------------------------------------------------------------

class ValidatedSoftwareListView(generic.ObjectListView):
    queryset = ValidatedSoftware.objects.all()
    table = tables.ValidatedSoftwareTable
    filterset = filtersets.ValidatedSoftwareFilterSet
    filterset_form = forms.ValidatedSoftwareFilterForm


class ValidatedSoftwareView(generic.ObjectView):
    queryset = ValidatedSoftware.objects.all()


class ValidatedSoftwareEditView(generic.ObjectEditView):
    queryset = ValidatedSoftware.objects.all()
    form = forms.ValidatedSoftwareForm


class ValidatedSoftwareDeleteView(generic.ObjectDeleteView):
    queryset = ValidatedSoftware.objects.all()


class ValidatedSoftwareBulkDeleteView(generic.BulkDeleteView):
    queryset = ValidatedSoftware.objects.all()
    table = tables.ValidatedSoftwareTable
    filterset = filtersets.ValidatedSoftwareFilterSet


# -----------------------------------------------------------------------------
# CVE
# -----------------------------------------------------------------------------

class CVEListView(generic.ObjectListView):
    queryset = CVE.objects.all()
    table = tables.CVETable
    filterset = filtersets.CVEFilterSet
    filterset_form = forms.CVEFilterForm


class CVEView(generic.ObjectView):
    queryset = CVE.objects.all()

    def get_extra_context(self, request, instance):
        return {"vulnerabilities": instance.vulnerabilities.all()}


class CVEEditView(generic.ObjectEditView):
    queryset = CVE.objects.all()
    form = forms.CVEForm


class CVEDeleteView(generic.ObjectDeleteView):
    queryset = CVE.objects.all()


class CVEBulkDeleteView(generic.BulkDeleteView):
    queryset = CVE.objects.all()
    table = tables.CVETable
    filterset = filtersets.CVEFilterSet


# -----------------------------------------------------------------------------
# Vulnerability
# -----------------------------------------------------------------------------

class VulnerabilityListView(generic.ObjectListView):
    queryset = Vulnerability.objects.all()
    table = tables.VulnerabilityTable
    filterset = filtersets.VulnerabilityFilterSet
    filterset_form = forms.VulnerabilityFilterForm


class VulnerabilityView(generic.ObjectView):
    queryset = Vulnerability.objects.all()


class VulnerabilityEditView(generic.ObjectEditView):
    queryset = Vulnerability.objects.all()
    form = forms.VulnerabilityForm


class VulnerabilityDeleteView(generic.ObjectDeleteView):
    queryset = Vulnerability.objects.all()


class VulnerabilityBulkDeleteView(generic.BulkDeleteView):
    queryset = Vulnerability.objects.all()
    table = tables.VulnerabilityTable
    filterset = filtersets.VulnerabilityFilterSet
