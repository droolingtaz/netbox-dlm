import django_tables2 as tables

from netbox.tables import NetBoxTable, columns

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


class ProviderTable(NetBoxTable):
    name = tables.Column(linkify=True)
    contract_count = tables.Column(verbose_name="Contracts", empty_values=())
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Provider
        fields = ("pk", "id", "name", "phone", "email", "portal_url", "contract_count", "tags")
        default_columns = ("name", "phone", "email", "contract_count")

    def render_contract_count(self, record):
        return record.contracts.count()


class ContractTable(NetBoxTable):
    name = tables.Column(linkify=True)
    provider = tables.Column(linkify=True)
    device_count = tables.Column(verbose_name="Devices", empty_values=(), accessor="devices__count")
    end_date = tables.Column()
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Contract
        fields = (
            "pk", "id", "name", "provider", "contract_number", "support_level",
            "start_date", "end_date", "cost", "currency", "device_count", "tags",
        )
        default_columns = ("name", "provider", "support_level", "end_date", "device_count")

    def render_end_date(self, value, record):
        if record.expired:
            return f"{value} (expired)"
        if record.expiring_soon:
            return f"{value} (expiring soon)"
        return value


class HardwareNoticeTable(NetBoxTable):
    target = tables.Column(linkify=True, order_by=("device_type", "module_type"))
    end_of_support = tables.Column()
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = HardwareNotice
        fields = (
            "pk", "id", "target", "end_of_sale", "end_of_support",
            "end_of_security_patches", "end_of_sw_releases", "documentation_url", "tags",
        )
        default_columns = ("target", "end_of_sale", "end_of_support", "end_of_security_patches")

    def render_end_of_support(self, value, record):
        if record.end_of_support_passed:
            return f"{value} (past)"
        return value


class SoftwareVersionTable(NetBoxTable):
    display = tables.Column(linkify=True, verbose_name="Software Version")
    platform = tables.Column(linkify=True)
    long_term_support = columns.BooleanColumn(verbose_name="LTS")
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = SoftwareVersion
        fields = (
            "pk", "id", "display", "platform", "version", "release_date",
            "end_of_support", "long_term_support", "documentation_url", "tags",
        )
        default_columns = ("display", "platform", "version", "release_date", "end_of_support", "long_term_support")


class SoftwareImageFileTable(NetBoxTable):
    file_name = tables.Column(linkify=True)
    software_version = tables.Column(linkify=True)
    default_image = columns.BooleanColumn()
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = SoftwareImageFile
        fields = (
            "pk", "id", "file_name", "software_version", "hashing_algorithm",
            "checksum", "file_size", "default_image", "tags",
        )
        default_columns = ("file_name", "software_version", "hashing_algorithm", "default_image")


class DeviceSoftwareTable(NetBoxTable):
    device = tables.Column(linkify=True)
    software_version = tables.Column(linkify=True)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = DeviceSoftware
        fields = ("pk", "id", "device", "software_version", "last_checked", "tags")
        default_columns = ("device", "software_version", "last_checked")


class ValidatedSoftwareTable(NetBoxTable):
    software_version = tables.Column(linkify=True)
    preferred = columns.BooleanColumn()
    valid_now = columns.BooleanColumn(orderable=False)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = ValidatedSoftware
        fields = ("pk", "id", "software_version", "start", "end", "preferred", "valid_now", "tags")
        default_columns = ("software_version", "start", "end", "preferred", "valid_now")


class CVETable(NetBoxTable):
    cve_id = tables.Column(linkify=True)
    severity = columns.ChoiceFieldColumn()
    status = columns.ChoiceFieldColumn()
    vulnerability_count = tables.Column(
        verbose_name="Vulnerabilities", empty_values=(), accessor="vulnerabilities__count"
    )
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = CVE
        fields = (
            "pk", "id", "cve_id", "name", "severity", "status", "cvss_score",
            "published_date", "link", "vulnerability_count", "tags",
        )
        default_columns = ("cve_id", "name", "severity", "status", "cvss_score", "vulnerability_count")


class VulnerabilityTable(NetBoxTable):
    cve = tables.Column(linkify=True)
    software_version = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    status = columns.ChoiceFieldColumn()
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Vulnerability
        fields = ("pk", "id", "cve", "software_version", "device", "status", "tags")
        default_columns = ("cve", "software_version", "device", "status")
