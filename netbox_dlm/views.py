from django.db.models import Count

from netbox.views import generic
from utilities.views import register_model_view

from . import filtersets, forms, tables
from .models import (
    CVE,
    Contract,
    DeviceSoftware,
    HardwareNotice,
    InventoryItemRolePlatform,
    InventoryItemSoftware,
    Provider,
    SoftwareImageFile,
    SoftwareVersion,
    ValidatedSoftware,
    Vulnerability,
)


# -----------------------------------------------------------------------------
# Provider
# -----------------------------------------------------------------------------

@register_model_view(Provider, "list", path="", detail=False)
class ProviderListView(generic.ObjectListView):
    queryset = Provider.objects.all()
    table = tables.ProviderTable
    filterset = filtersets.ProviderFilterSet


@register_model_view(Provider)
class ProviderView(generic.ObjectView):
    queryset = Provider.objects.all()


@register_model_view(Provider, "add", detail=False)
@register_model_view(Provider, "edit")
class ProviderEditView(generic.ObjectEditView):
    queryset = Provider.objects.all()
    form = forms.ProviderForm


@register_model_view(Provider, "delete")
class ProviderDeleteView(generic.ObjectDeleteView):
    queryset = Provider.objects.all()


@register_model_view(Provider, "bulk_delete", path="delete", detail=False)
class ProviderBulkDeleteView(generic.BulkDeleteView):
    queryset = Provider.objects.all()
    table = tables.ProviderTable
    filterset = filtersets.ProviderFilterSet


# -----------------------------------------------------------------------------
# Contract
# -----------------------------------------------------------------------------

@register_model_view(Contract, "list", path="", detail=False)
class ContractListView(generic.ObjectListView):
    queryset = Contract.objects.all()
    table = tables.ContractTable
    filterset = filtersets.ContractFilterSet
    filterset_form = forms.ContractFilterForm


@register_model_view(Contract)
class ContractView(generic.ObjectView):
    queryset = Contract.objects.all()


@register_model_view(Contract, "add", detail=False)
@register_model_view(Contract, "edit")
class ContractEditView(generic.ObjectEditView):
    queryset = Contract.objects.all()
    form = forms.ContractForm


@register_model_view(Contract, "delete")
class ContractDeleteView(generic.ObjectDeleteView):
    queryset = Contract.objects.all()


@register_model_view(Contract, "bulk_delete", path="delete", detail=False)
class ContractBulkDeleteView(generic.BulkDeleteView):
    queryset = Contract.objects.all()
    table = tables.ContractTable
    filterset = filtersets.ContractFilterSet


# -----------------------------------------------------------------------------
# HardwareNotice
# -----------------------------------------------------------------------------

@register_model_view(HardwareNotice, "list", path="", detail=False)
class HardwareNoticeListView(generic.ObjectListView):
    queryset = HardwareNotice.objects.all()
    table = tables.HardwareNoticeTable
    filterset = filtersets.HardwareNoticeFilterSet
    filterset_form = forms.HardwareNoticeFilterForm


@register_model_view(HardwareNotice)
class HardwareNoticeView(generic.ObjectView):
    queryset = HardwareNotice.objects.all()


@register_model_view(HardwareNotice, "add", detail=False)
@register_model_view(HardwareNotice, "edit")
class HardwareNoticeEditView(generic.ObjectEditView):
    queryset = HardwareNotice.objects.all()
    form = forms.HardwareNoticeForm


@register_model_view(HardwareNotice, "delete")
class HardwareNoticeDeleteView(generic.ObjectDeleteView):
    queryset = HardwareNotice.objects.all()


@register_model_view(HardwareNotice, "bulk_delete", path="delete", detail=False)
class HardwareNoticeBulkDeleteView(generic.BulkDeleteView):
    queryset = HardwareNotice.objects.all()
    table = tables.HardwareNoticeTable
    filterset = filtersets.HardwareNoticeFilterSet


# -----------------------------------------------------------------------------
# SoftwareVersion
# -----------------------------------------------------------------------------

@register_model_view(SoftwareVersion, "list", path="", detail=False)
class SoftwareVersionListView(generic.ObjectListView):
    queryset = SoftwareVersion.objects.annotate(
        device_count=Count("devices_running", distinct=True),
        inventory_item_count=Count("inventory_items_running", distinct=True),
    )
    table = tables.SoftwareVersionTable
    filterset = filtersets.SoftwareVersionFilterSet
    filterset_form = forms.SoftwareVersionFilterForm


@register_model_view(SoftwareVersion)
class SoftwareVersionView(generic.ObjectView):
    queryset = SoftwareVersion.objects.all()

    def get_extra_context(self, request, instance):
        return {
            "image_files": instance.image_files.all(),
            "validated_rules": instance.validated_rules.all(),
            "cves": instance.cves.all(),
            "devices_running": instance.devices_running.select_related("device"),
        }


@register_model_view(SoftwareVersion, "add", detail=False)
@register_model_view(SoftwareVersion, "edit")
class SoftwareVersionEditView(generic.ObjectEditView):
    queryset = SoftwareVersion.objects.all()
    form = forms.SoftwareVersionForm


@register_model_view(SoftwareVersion, "delete")
class SoftwareVersionDeleteView(generic.ObjectDeleteView):
    queryset = SoftwareVersion.objects.all()


@register_model_view(SoftwareVersion, "bulk_delete", path="delete", detail=False)
class SoftwareVersionBulkDeleteView(generic.BulkDeleteView):
    queryset = SoftwareVersion.objects.annotate(
        device_count=Count("devices_running", distinct=True),
        inventory_item_count=Count("inventory_items_running", distinct=True),
    )
    table = tables.SoftwareVersionTable
    filterset = filtersets.SoftwareVersionFilterSet


# -----------------------------------------------------------------------------
# SoftwareImageFile
# -----------------------------------------------------------------------------

@register_model_view(SoftwareImageFile, "list", path="", detail=False)
class SoftwareImageFileListView(generic.ObjectListView):
    queryset = SoftwareImageFile.objects.all()
    table = tables.SoftwareImageFileTable
    filterset = filtersets.SoftwareImageFileFilterSet
    filterset_form = forms.SoftwareImageFileFilterForm


@register_model_view(SoftwareImageFile)
class SoftwareImageFileView(generic.ObjectView):
    queryset = SoftwareImageFile.objects.all()


@register_model_view(SoftwareImageFile, "add", detail=False)
@register_model_view(SoftwareImageFile, "edit")
class SoftwareImageFileEditView(generic.ObjectEditView):
    queryset = SoftwareImageFile.objects.all()
    form = forms.SoftwareImageFileForm


@register_model_view(SoftwareImageFile, "delete")
class SoftwareImageFileDeleteView(generic.ObjectDeleteView):
    queryset = SoftwareImageFile.objects.all()


@register_model_view(SoftwareImageFile, "bulk_delete", path="delete", detail=False)
class SoftwareImageFileBulkDeleteView(generic.BulkDeleteView):
    queryset = SoftwareImageFile.objects.all()
    table = tables.SoftwareImageFileTable
    filterset = filtersets.SoftwareImageFileFilterSet


# -----------------------------------------------------------------------------
# DeviceSoftware
# -----------------------------------------------------------------------------

@register_model_view(DeviceSoftware, "list", path="", detail=False)
class DeviceSoftwareListView(generic.ObjectListView):
    queryset = DeviceSoftware.objects.all()
    table = tables.DeviceSoftwareTable
    filterset = filtersets.DeviceSoftwareFilterSet
    filterset_form = forms.DeviceSoftwareFilterForm


@register_model_view(DeviceSoftware)
class DeviceSoftwareView(generic.ObjectView):
    queryset = DeviceSoftware.objects.all()


@register_model_view(DeviceSoftware, "add", detail=False)
@register_model_view(DeviceSoftware, "edit")
class DeviceSoftwareEditView(generic.ObjectEditView):
    queryset = DeviceSoftware.objects.all()
    form = forms.DeviceSoftwareForm


@register_model_view(DeviceSoftware, "delete")
class DeviceSoftwareDeleteView(generic.ObjectDeleteView):
    queryset = DeviceSoftware.objects.all()


@register_model_view(DeviceSoftware, "bulk_delete", path="delete", detail=False)
class DeviceSoftwareBulkDeleteView(generic.BulkDeleteView):
    queryset = DeviceSoftware.objects.all()
    table = tables.DeviceSoftwareTable
    filterset = filtersets.DeviceSoftwareFilterSet


# -----------------------------------------------------------------------------
# InventoryItemRolePlatform
# -----------------------------------------------------------------------------

@register_model_view(InventoryItemRolePlatform, "list", path="", detail=False)
class InventoryItemRolePlatformListView(generic.ObjectListView):
    queryset = InventoryItemRolePlatform.objects.all()
    table = tables.InventoryItemRolePlatformTable
    filterset = filtersets.InventoryItemRolePlatformFilterSet
    filterset_form = forms.InventoryItemRolePlatformFilterForm


@register_model_view(InventoryItemRolePlatform)
class InventoryItemRolePlatformView(generic.ObjectView):
    queryset = InventoryItemRolePlatform.objects.all()


@register_model_view(InventoryItemRolePlatform, "add", detail=False)
@register_model_view(InventoryItemRolePlatform, "edit")
class InventoryItemRolePlatformEditView(generic.ObjectEditView):
    queryset = InventoryItemRolePlatform.objects.all()
    form = forms.InventoryItemRolePlatformForm


@register_model_view(InventoryItemRolePlatform, "delete")
class InventoryItemRolePlatformDeleteView(generic.ObjectDeleteView):
    queryset = InventoryItemRolePlatform.objects.all()


@register_model_view(InventoryItemRolePlatform, "bulk_delete", path="delete", detail=False)
class InventoryItemRolePlatformBulkDeleteView(generic.BulkDeleteView):
    queryset = InventoryItemRolePlatform.objects.all()
    table = tables.InventoryItemRolePlatformTable
    filterset = filtersets.InventoryItemRolePlatformFilterSet


# -----------------------------------------------------------------------------
# InventoryItemSoftware
# -----------------------------------------------------------------------------

@register_model_view(InventoryItemSoftware, "list", path="", detail=False)
class InventoryItemSoftwareListView(generic.ObjectListView):
    queryset = InventoryItemSoftware.objects.all()
    table = tables.InventoryItemSoftwareTable
    filterset = filtersets.InventoryItemSoftwareFilterSet
    filterset_form = forms.InventoryItemSoftwareFilterForm


@register_model_view(InventoryItemSoftware)
class InventoryItemSoftwareView(generic.ObjectView):
    queryset = InventoryItemSoftware.objects.all()


@register_model_view(InventoryItemSoftware, "add", detail=False)
@register_model_view(InventoryItemSoftware, "edit")
class InventoryItemSoftwareEditView(generic.ObjectEditView):
    queryset = InventoryItemSoftware.objects.all()
    form = forms.InventoryItemSoftwareForm


@register_model_view(InventoryItemSoftware, "delete")
class InventoryItemSoftwareDeleteView(generic.ObjectDeleteView):
    queryset = InventoryItemSoftware.objects.all()


@register_model_view(InventoryItemSoftware, "bulk_delete", path="delete", detail=False)
class InventoryItemSoftwareBulkDeleteView(generic.BulkDeleteView):
    queryset = InventoryItemSoftware.objects.all()
    table = tables.InventoryItemSoftwareTable
    filterset = filtersets.InventoryItemSoftwareFilterSet


# -----------------------------------------------------------------------------
# ValidatedSoftware
# -----------------------------------------------------------------------------

@register_model_view(ValidatedSoftware, "list", path="", detail=False)
class ValidatedSoftwareListView(generic.ObjectListView):
    queryset = ValidatedSoftware.objects.all()
    table = tables.ValidatedSoftwareTable
    filterset = filtersets.ValidatedSoftwareFilterSet
    filterset_form = forms.ValidatedSoftwareFilterForm


@register_model_view(ValidatedSoftware)
class ValidatedSoftwareView(generic.ObjectView):
    queryset = ValidatedSoftware.objects.all()


@register_model_view(ValidatedSoftware, "add", detail=False)
@register_model_view(ValidatedSoftware, "edit")
class ValidatedSoftwareEditView(generic.ObjectEditView):
    queryset = ValidatedSoftware.objects.all()
    form = forms.ValidatedSoftwareForm


@register_model_view(ValidatedSoftware, "delete")
class ValidatedSoftwareDeleteView(generic.ObjectDeleteView):
    queryset = ValidatedSoftware.objects.all()


@register_model_view(ValidatedSoftware, "bulk_delete", path="delete", detail=False)
class ValidatedSoftwareBulkDeleteView(generic.BulkDeleteView):
    queryset = ValidatedSoftware.objects.all()
    table = tables.ValidatedSoftwareTable
    filterset = filtersets.ValidatedSoftwareFilterSet


# -----------------------------------------------------------------------------
# CVE
# -----------------------------------------------------------------------------

@register_model_view(CVE, "list", path="", detail=False)
class CVEListView(generic.ObjectListView):
    queryset = CVE.objects.annotate(vulnerability_count=Count("vulnerabilities", distinct=True))
    table = tables.CVETable
    filterset = filtersets.CVEFilterSet
    filterset_form = forms.CVEFilterForm


@register_model_view(CVE)
class CVEView(generic.ObjectView):
    queryset = CVE.objects.all()

    def get_extra_context(self, request, instance):
        vulnerabilities_table = tables.VulnerabilityTable(
            instance.vulnerabilities.all(), exclude=("cve",)
        )
        vulnerabilities_table.configure(request)
        return {"vulnerabilities_table": vulnerabilities_table}


@register_model_view(CVE, "add", detail=False)
@register_model_view(CVE, "edit")
class CVEEditView(generic.ObjectEditView):
    queryset = CVE.objects.all()
    form = forms.CVEForm


@register_model_view(CVE, "delete")
class CVEDeleteView(generic.ObjectDeleteView):
    queryset = CVE.objects.all()


@register_model_view(CVE, "bulk_delete", path="delete", detail=False)
class CVEBulkDeleteView(generic.BulkDeleteView):
    queryset = CVE.objects.annotate(vulnerability_count=Count("vulnerabilities", distinct=True))
    table = tables.CVETable
    filterset = filtersets.CVEFilterSet


# -----------------------------------------------------------------------------
# Vulnerability
# -----------------------------------------------------------------------------

@register_model_view(Vulnerability, "list", path="", detail=False)
class VulnerabilityListView(generic.ObjectListView):
    queryset = Vulnerability.objects.all()
    table = tables.VulnerabilityTable
    filterset = filtersets.VulnerabilityFilterSet
    filterset_form = forms.VulnerabilityFilterForm


@register_model_view(Vulnerability)
class VulnerabilityView(generic.ObjectView):
    queryset = Vulnerability.objects.all()


@register_model_view(Vulnerability, "add", detail=False)
@register_model_view(Vulnerability, "edit")
class VulnerabilityEditView(generic.ObjectEditView):
    queryset = Vulnerability.objects.all()
    form = forms.VulnerabilityForm


@register_model_view(Vulnerability, "delete")
class VulnerabilityDeleteView(generic.ObjectDeleteView):
    queryset = Vulnerability.objects.all()


@register_model_view(Vulnerability, "bulk_delete", path="delete", detail=False)
class VulnerabilityBulkDeleteView(generic.BulkDeleteView):
    queryset = Vulnerability.objects.all()
    table = tables.VulnerabilityTable
    filterset = filtersets.VulnerabilityFilterSet
