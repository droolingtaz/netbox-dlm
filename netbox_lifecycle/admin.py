from django.contrib import admin

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


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "portal_url")
    search_fields = ("name", "email")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "support_level", "start_date", "end_date")
    list_filter = ("provider", "support_level")
    search_fields = ("name", "contract_number")


@admin.register(HardwareNotice)
class HardwareNoticeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "end_of_sale", "end_of_support", "end_of_security_patches")
    list_filter = ("end_of_support",)


@admin.register(SoftwareVersion)
class SoftwareVersionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "platform", "version", "release_date", "end_of_support", "long_term_support")
    list_filter = ("platform", "long_term_support")
    search_fields = ("version", "alias")


@admin.register(SoftwareImageFile)
class SoftwareImageFileAdmin(admin.ModelAdmin):
    list_display = ("file_name", "software_version", "hashing_algorithm", "default_image")
    list_filter = ("hashing_algorithm", "default_image")
    search_fields = ("file_name", "checksum")


@admin.register(DeviceSoftware)
class DeviceSoftwareAdmin(admin.ModelAdmin):
    list_display = ("device", "software_version", "last_checked")
    search_fields = ("device__name",)


@admin.register(ValidatedSoftware)
class ValidatedSoftwareAdmin(admin.ModelAdmin):
    list_display = ("software_version", "start", "end", "preferred", "valid_now")
    list_filter = ("preferred",)


@admin.register(CVE)
class CVEAdmin(admin.ModelAdmin):
    list_display = ("cve_id", "name", "severity", "status", "cvss_score", "published_date")
    list_filter = ("severity", "status")
    search_fields = ("cve_id", "name", "description")


@admin.register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):
    list_display = ("cve", "software_version", "device", "status")
    list_filter = ("status",)
    search_fields = ("cve__cve_id", "device__name")
