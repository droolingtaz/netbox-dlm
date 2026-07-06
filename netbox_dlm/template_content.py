from netbox.plugins import PluginTemplateExtension

from .models import DeviceSoftware, HardwareNotice, ValidatedSoftware, Vulnerability


class DeviceLifecyclePanel(PluginTemplateExtension):
    """Adds a lifecycle summary panel to the Device detail view."""

    models = ["dcim.device"]

    def right_page(self):
        device = self.context["object"]
        software = DeviceSoftware.objects.filter(device=device).select_related("software_version").first()
        hardware_notice = HardwareNotice.objects.filter(device_type=device.device_type).first()
        vulnerabilities = Vulnerability.objects.filter(device=device).exclude(status="resolved")

        validated_rules = []
        if software:
            validated_rules = [
                rule
                for rule in ValidatedSoftware.objects.filter(software_version=software.software_version)
                if rule.valid_now and rule.covers_device(device)
            ]

        return self.render(
            "netbox_dlm/device_lifecycle_panel.html",
            extra_context={
                "software": software,
                "hardware_notice": hardware_notice,
                "vulnerabilities": vulnerabilities,
                "validated_rules": validated_rules,
            },
        )


class DeviceTypeLifecyclePanel(PluginTemplateExtension):
    """Adds a hardware end-of-life panel to the DeviceType detail view."""

    models = ["dcim.devicetype"]

    def right_page(self):
        device_type = self.context["object"]
        hardware_notice = HardwareNotice.objects.filter(device_type=device_type).first()
        return self.render(
            "netbox_dlm/devicetype_lifecycle_panel.html",
            extra_context={"hardware_notice": hardware_notice},
        )


template_extensions = [DeviceLifecyclePanel, DeviceTypeLifecyclePanel]
