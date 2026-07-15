from netbox.plugins import PluginConfig


class DeviceLifecycleConfig(PluginConfig):
    name = "netbox_dlm"
    verbose_name = "Device Lifecycle Management"
    description = (
        "Track hardware end-of-life/end-of-support notices, software versions and "
        "validated-software compliance, CVE/vulnerability exposure, and maintenance "
        "contracts — modeled after Nautobot's Device Lifecycle Management app."
    )
    version = "0.4.1"
    base_url = "device-lifecycle"
    min_version = "4.1.0"
    default_settings = {
        # Set to a NIST NVD API key to raise CVE-lookup rate limits (optional).
        "nist_api_key": None,
        # How many days out a hardware/software EoS date counts as "upcoming"
        # for dashboard highlighting.
        "eos_warning_days": 180,
    }


config = DeviceLifecycleConfig
