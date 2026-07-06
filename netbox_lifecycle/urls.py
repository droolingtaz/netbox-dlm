from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from . import models, views

urlpatterns = [
    # Provider
    path("providers/", views.ProviderListView.as_view(), name="provider_list"),
    path("providers/add/", views.ProviderEditView.as_view(), name="provider_add"),
    path("providers/<int:pk>/", views.ProviderView.as_view(), name="provider"),
    path("providers/<int:pk>/edit/", views.ProviderEditView.as_view(), name="provider_edit"),
    path("providers/<int:pk>/delete/", views.ProviderDeleteView.as_view(), name="provider_delete"),
    path("providers/delete/", views.ProviderBulkDeleteView.as_view(), name="provider_bulk_delete"),
    path(
        "providers/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="provider_changelog",
        kwargs={"model": models.Provider},
    ),

    # Contract
    path("contracts/", views.ContractListView.as_view(), name="contract_list"),
    path("contracts/add/", views.ContractEditView.as_view(), name="contract_add"),
    path("contracts/<int:pk>/", views.ContractView.as_view(), name="contract"),
    path("contracts/<int:pk>/edit/", views.ContractEditView.as_view(), name="contract_edit"),
    path("contracts/<int:pk>/delete/", views.ContractDeleteView.as_view(), name="contract_delete"),
    path("contracts/delete/", views.ContractBulkDeleteView.as_view(), name="contract_bulk_delete"),
    path(
        "contracts/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="contract_changelog",
        kwargs={"model": models.Contract},
    ),

    # HardwareNotice
    path("hardware-notices/", views.HardwareNoticeListView.as_view(), name="hardwarenotice_list"),
    path("hardware-notices/add/", views.HardwareNoticeEditView.as_view(), name="hardwarenotice_add"),
    path("hardware-notices/<int:pk>/", views.HardwareNoticeView.as_view(), name="hardwarenotice"),
    path("hardware-notices/<int:pk>/edit/", views.HardwareNoticeEditView.as_view(), name="hardwarenotice_edit"),
    path("hardware-notices/<int:pk>/delete/", views.HardwareNoticeDeleteView.as_view(), name="hardwarenotice_delete"),
    path("hardware-notices/delete/", views.HardwareNoticeBulkDeleteView.as_view(), name="hardwarenotice_bulk_delete"),
    path(
        "hardware-notices/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="hardwarenotice_changelog",
        kwargs={"model": models.HardwareNotice},
    ),

    # SoftwareVersion
    path("software-versions/", views.SoftwareVersionListView.as_view(), name="softwareversion_list"),
    path("software-versions/add/", views.SoftwareVersionEditView.as_view(), name="softwareversion_add"),
    path("software-versions/<int:pk>/", views.SoftwareVersionView.as_view(), name="softwareversion"),
    path("software-versions/<int:pk>/edit/", views.SoftwareVersionEditView.as_view(), name="softwareversion_edit"),
    path("software-versions/<int:pk>/delete/", views.SoftwareVersionDeleteView.as_view(), name="softwareversion_delete"),
    path("software-versions/delete/", views.SoftwareVersionBulkDeleteView.as_view(), name="softwareversion_bulk_delete"),
    path(
        "software-versions/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="softwareversion_changelog",
        kwargs={"model": models.SoftwareVersion},
    ),

    # SoftwareImageFile
    path("software-images/", views.SoftwareImageFileListView.as_view(), name="softwareimagefile_list"),
    path("software-images/add/", views.SoftwareImageFileEditView.as_view(), name="softwareimagefile_add"),
    path("software-images/<int:pk>/", views.SoftwareImageFileView.as_view(), name="softwareimagefile"),
    path("software-images/<int:pk>/edit/", views.SoftwareImageFileEditView.as_view(), name="softwareimagefile_edit"),
    path("software-images/<int:pk>/delete/", views.SoftwareImageFileDeleteView.as_view(), name="softwareimagefile_delete"),
    path("software-images/delete/", views.SoftwareImageFileBulkDeleteView.as_view(), name="softwareimagefile_bulk_delete"),
    path(
        "software-images/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="softwareimagefile_changelog",
        kwargs={"model": models.SoftwareImageFile},
    ),

    # DeviceSoftware
    path("device-software/", views.DeviceSoftwareListView.as_view(), name="devicesoftware_list"),
    path("device-software/add/", views.DeviceSoftwareEditView.as_view(), name="devicesoftware_add"),
    path("device-software/<int:pk>/", views.DeviceSoftwareView.as_view(), name="devicesoftware"),
    path("device-software/<int:pk>/edit/", views.DeviceSoftwareEditView.as_view(), name="devicesoftware_edit"),
    path("device-software/<int:pk>/delete/", views.DeviceSoftwareDeleteView.as_view(), name="devicesoftware_delete"),
    path("device-software/delete/", views.DeviceSoftwareBulkDeleteView.as_view(), name="devicesoftware_bulk_delete"),
    path(
        "device-software/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="devicesoftware_changelog",
        kwargs={"model": models.DeviceSoftware},
    ),

    # ValidatedSoftware
    path("validated-software/", views.ValidatedSoftwareListView.as_view(), name="validatedsoftware_list"),
    path("validated-software/add/", views.ValidatedSoftwareEditView.as_view(), name="validatedsoftware_add"),
    path("validated-software/<int:pk>/", views.ValidatedSoftwareView.as_view(), name="validatedsoftware"),
    path("validated-software/<int:pk>/edit/", views.ValidatedSoftwareEditView.as_view(), name="validatedsoftware_edit"),
    path("validated-software/<int:pk>/delete/", views.ValidatedSoftwareDeleteView.as_view(), name="validatedsoftware_delete"),
    path("validated-software/delete/", views.ValidatedSoftwareBulkDeleteView.as_view(), name="validatedsoftware_bulk_delete"),
    path(
        "validated-software/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="validatedsoftware_changelog",
        kwargs={"model": models.ValidatedSoftware},
    ),

    # CVE
    path("cves/", views.CVEListView.as_view(), name="cve_list"),
    path("cves/add/", views.CVEEditView.as_view(), name="cve_add"),
    path("cves/<int:pk>/", views.CVEView.as_view(), name="cve"),
    path("cves/<int:pk>/edit/", views.CVEEditView.as_view(), name="cve_edit"),
    path("cves/<int:pk>/delete/", views.CVEDeleteView.as_view(), name="cve_delete"),
    path("cves/delete/", views.CVEBulkDeleteView.as_view(), name="cve_bulk_delete"),
    path(
        "cves/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="cve_changelog",
        kwargs={"model": models.CVE},
    ),

    # Vulnerability
    path("vulnerabilities/", views.VulnerabilityListView.as_view(), name="vulnerability_list"),
    path("vulnerabilities/add/", views.VulnerabilityEditView.as_view(), name="vulnerability_add"),
    path("vulnerabilities/<int:pk>/", views.VulnerabilityView.as_view(), name="vulnerability"),
    path("vulnerabilities/<int:pk>/edit/", views.VulnerabilityEditView.as_view(), name="vulnerability_edit"),
    path("vulnerabilities/<int:pk>/delete/", views.VulnerabilityDeleteView.as_view(), name="vulnerability_delete"),
    path("vulnerabilities/delete/", views.VulnerabilityBulkDeleteView.as_view(), name="vulnerability_bulk_delete"),
    path(
        "vulnerabilities/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="vulnerability_changelog",
        kwargs={"model": models.Vulnerability},
    ),
]
