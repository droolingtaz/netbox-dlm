from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

hardware_items = (
    PluginMenuItem(
        link="plugins:netbox_dlm:hardwarenotice_list",
        link_text="Hardware Notices",
        permissions=["netbox_dlm.view_hardwarenotice"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:hardwarenotice_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_hardwarenotice"],
            ),
        ),
    ),
)

software_items = (
    PluginMenuItem(
        link="plugins:netbox_dlm:softwareversion_list",
        link_text="Software Versions",
        permissions=["netbox_dlm.view_softwareversion"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:softwareversion_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_softwareversion"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:softwareimagefile_list",
        link_text="Software Images",
        permissions=["netbox_dlm.view_softwareimagefile"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:softwareimagefile_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_softwareimagefile"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:devicesoftware_list",
        link_text="Device Software",
        permissions=["netbox_dlm.view_devicesoftware"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:devicesoftware_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_devicesoftware"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:inventoryitemsoftware_list",
        link_text="Inventory Item Software",
        permissions=["netbox_dlm.view_inventoryitemsoftware"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:inventoryitemsoftware_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_inventoryitemsoftware"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:inventoryitemroleplatform_list",
        link_text="Inventory Item Role Platforms",
        permissions=["netbox_dlm.view_inventoryitemroleplatform"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:inventoryitemroleplatform_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_inventoryitemroleplatform"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:validatedsoftware_list",
        link_text="Validated Software",
        permissions=["netbox_dlm.view_validatedsoftware"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:validatedsoftware_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_validatedsoftware"],
            ),
        ),
    ),
)

cve_items = (
    PluginMenuItem(
        link="plugins:netbox_dlm:cve_list",
        link_text="CVEs",
        permissions=["netbox_dlm.view_cve"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:cve_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_cve"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:vulnerability_list",
        link_text="Vulnerabilities",
        permissions=["netbox_dlm.view_vulnerability"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:vulnerability_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_vulnerability"],
            ),
        ),
    ),
)

contract_items = (
    PluginMenuItem(
        link="plugins:netbox_dlm:provider_list",
        link_text="Providers",
        permissions=["netbox_dlm.view_provider"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:provider_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_provider"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dlm:contract_list",
        link_text="Contracts",
        permissions=["netbox_dlm.view_contract"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_dlm:contract_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_dlm.add_contract"],
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
