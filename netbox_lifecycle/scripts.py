"""
Custom Scripts for the Device Lifecycle Management plugin.

NetBox auto-discovers a `scripts` module inside an installed plugin and
surfaces its Script subclasses under Operations > Scripts, grouped under
this plugin's name. Run these on a schedule (e.g. via NetBox's built-in
Scheduled Jobs, or cron + `manage.py runscript`) to keep compliance data fresh.
"""
import datetime

from django.utils import timezone
from extras.scripts import BooleanVar, IntegerVar, Script

from .models import CVE, DeviceSoftware, HardwareNotice, ValidatedSoftware, Vulnerability


class CheckHardwareNotices(Script):
    class Meta:
        name = "Check Hardware Notices"
        description = (
            "Scans all HardwareNotice records and reports device types / module "
            "types that have passed end-of-support, or are approaching it."
        )

    warning_days = IntegerVar(
        description="Flag notices with end_of_support within this many days",
        default=180,
        required=False,
    )

    def run(self, data, commit):
        warning_days = data.get("warning_days") or 180
        today = timezone.localdate()
        horizon = today + datetime.timedelta(days=warning_days)

        past_due = HardwareNotice.objects.filter(end_of_support__lt=today)
        upcoming = HardwareNotice.objects.filter(
            end_of_support__gte=today, end_of_support__lte=horizon
        )

        for notice in past_due:
            device_count = 0
            if notice.device_type_id:
                device_count = notice.device_type.instances.count()
            self.log_failure(
                f"{notice.target} is past end-of-support ({notice.end_of_support}), "
                f"affecting {device_count} device(s)."
            )

        for notice in upcoming:
            self.log_warning(
                f"{notice.target} reaches end-of-support on {notice.end_of_support} "
                f"(within {warning_days} days)."
            )

        self.log_info(
            f"Checked {HardwareNotice.objects.count()} hardware notices: "
            f"{past_due.count()} past due, {upcoming.count()} upcoming."
        )


class RunSoftwareValidation(Script):
    class Meta:
        name = "Run Software Validation"
        description = (
            "Compares each device's currently-recorded software against "
            "ValidatedSoftware rules and reports any that are out of compliance "
            "or unrecognized."
        )

    def run(self, data, commit):
        checked = 0
        non_compliant = 0

        for record in DeviceSoftware.objects.select_related("device", "software_version"):
            checked += 1
            device = record.device
            rules = ValidatedSoftware.objects.filter(
                software_version=record.software_version
            )
            applicable = [r for r in rules if r.valid_now and r.covers_device(device)]

            if not applicable:
                non_compliant += 1
                self.log_failure(
                    f"{device}: running {record.software_version}, which has no "
                    f"currently-valid ValidatedSoftware rule covering it."
                )
            elif not any(r.preferred for r in applicable):
                self.log_warning(
                    f"{device}: running {record.software_version}, which is valid "
                    f"but not the preferred version for its scope."
                )
            else:
                self.log_success(f"{device}: running compliant, preferred software.")

        self.log_info(f"Checked {checked} devices, {non_compliant} non-compliant.")


class SyncCVEs(Script):
    """
    Placeholder for NIST NVD CVE ingestion, mirroring the DLM app's NIST
    integration. Requires network egress to services.nvd.nist.gov and an
    External Integration / Secret configured for the API key if you want
    higher rate limits. Wire up the actual HTTP calls once your NetBox
    instance has outbound access configured.
    """

    class Meta:
        name = "Sync CVEs from NIST NVD"
        description = (
            "Fetch new/updated CVEs for tracked SoftwareVersions from the NIST "
            "NVD API 2.0. Requires outbound network access; disabled by default."
        )

    dry_run = BooleanVar(description="Log what would be synced without saving", default=True)

    def run(self, data, commit):
        self.log_warning(
            "SyncCVEs is a placeholder — implement the NVD API 2.0 request/parsing "
            "logic here, then create/update CVE records and link affected_software."
        )
        self.log_info(
            f"Currently tracking {CVE.objects.count()} CVEs and "
            f"{Vulnerability.objects.count()} vulnerability instances."
        )
