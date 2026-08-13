from django.urls import reverse
from utilities.testing import APITestCase

from netbox_dlm.models import Provider


class ProviderAPITestCase(APITestCase):
    model = Provider

    def test_list_providers(self):
        Provider.objects.create(name="Acme Support")
        Provider.objects.create(name="Beta Networks")

        url = reverse("plugins-api:netbox_dlm-api:provider-list")
        response = self.client.get(url, **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_create_provider(self):
        self.add_permissions("netbox_dlm.add_provider")
        url = reverse("plugins-api:netbox_dlm-api:provider-list")
        data = {"name": "New Vendor", "email": "support@newvendor.example"}

        response = self.client.post(url, data, format="json", **self.header)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Provider.objects.count(), 1)
