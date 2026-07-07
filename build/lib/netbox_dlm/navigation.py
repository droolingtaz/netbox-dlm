from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

hardware_items = (
    PluginMenuItem(
        link="plugins:netbox_dlm:hardwarenotice_list",
        link_text="Hardware Notices",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:hardwarenotice_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
)

software_items = (
    PluginMenuItem(
        link="plugins:netbox_dlm:softwareversion_list",
        link_text="Software Versions",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:softwareversion_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:softwareimagefile_list",
        link_text="Software Images",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:softwareimagefile_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:devicesoftware_list",
        link_text="Device Software",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:devicesoftware_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:validatedsoftware_list",
        link_text="Validated Software",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:validatedsoftware_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
)

cve_items = (
    PluginMenuItem(
        link="plugins:netbox_dlm:cve_list",
        link_text="CVEs",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:cve_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:vulnerability_list",
        link_text="Vulnerabilities",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:vulnerability_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
)

contract_items = (
    PluginMenuItem(
        link="plugins:netbox_dlm:provider_list",
        link_text="Providers",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:provider_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:contract_list",
        link_text="Contracts",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:contract_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
)

menu = PluginMenu(
    label="Device Lifecycle",
    groups=(
        ("Hardware", hardware_items),
        ("Software", software_items),
        ("Security", cve_items),
        ("Contracts", contract_items),
    ),
    icon_class="mdi mdi-clock-alert-outline",
)
