from netbox.api.routers import NetBoxRouter

from . import views

app_name = "netbox_dlm-api"

router = NetBoxRouter()

router.register("providers", views.ProviderViewSet)
router.register("contracts", views.ContractViewSet)
router.register("hardware-notices", views.HardwareNoticeViewSet)
router.register("software-versions", views.SoftwareVersionViewSet)
router.register("software-images", views.SoftwareImageFileViewSet)
router.register("device-software", views.DeviceSoftwareViewSet)
router.register("validated-software", views.ValidatedSoftwareViewSet)
router.register("cves", views.CVEViewSet)
router.register("vulnerabilities", views.VulnerabilityViewSet)

urlpatterns = router.urls
