from django.urls import include, path

from utilities.urls import get_model_urls

app_name = "netbox_dlm"

urlpatterns = (
    path("providers/", include(get_model_urls("netbox_dlm", "provider", detail=False))),
    path("providers/<int:pk>/", include(get_model_urls("netbox_dlm", "provider"))),

    path("contracts/", include(get_model_urls("netbox_dlm", "contract", detail=False))),
    path("contracts/<int:pk>/", include(get_model_urls("netbox_dlm", "contract"))),

    path("hardware-notices/", include(get_model_urls("netbox_dlm", "hardwarenotice", detail=False))),
    path("hardware-notices/<int:pk>/", include(get_model_urls("netbox_dlm", "hardwarenotice"))),

    path("software-versions/", include(get_model_urls("netbox_dlm", "softwareversion", detail=False))),
    path("software-versions/<int:pk>/", include(get_model_urls("netbox_dlm", "softwareversion"))),

    path("software-images/", include(get_model_urls("netbox_dlm", "softwareimagefile", detail=False))),
    path("software-images/<int:pk>/", include(get_model_urls("netbox_dlm", "softwareimagefile"))),

    path("device-software/", include(get_model_urls("netbox_dlm", "devicesoftware", detail=False))),
    path("device-software/<int:pk>/", include(get_model_urls("netbox_dlm", "devicesoftware"))),

    path(
        "inventory-item-role-platforms/",
        include(get_model_urls("netbox_dlm", "inventoryitemroleplatform", detail=False)),
    ),
    path(
        "inventory-item-role-platforms/<int:pk>/",
        include(get_model_urls("netbox_dlm", "inventoryitemroleplatform")),
    ),

    path("inventory-item-software/", include(get_model_urls("netbox_dlm", "inventoryitemsoftware", detail=False))),
    path("inventory-item-software/<int:pk>/", include(get_model_urls("netbox_dlm", "inventoryitemsoftware"))),

    path("validated-software/", include(get_model_urls("netbox_dlm", "validatedsoftware", detail=False))),
    path("validated-software/<int:pk>/", include(get_model_urls("netbox_dlm", "validatedsoftware"))),

    path("cves/", include(get_model_urls("netbox_dlm", "cve", detail=False))),
    path("cves/<int:pk>/", include(get_model_urls("netbox_dlm", "cve"))),

    path("vulnerabilities/", include(get_model_urls("netbox_dlm", "vulnerability", detail=False))),
    path("vulnerabilities/<int:pk>/", include(get_model_urls("netbox_dlm", "vulnerability"))),
)
