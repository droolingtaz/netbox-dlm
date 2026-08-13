import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from dcim.models import (
    Device,
    DeviceRole,
    DeviceType,
    Manufacturer,
    Platform,
    Site,
)

from netbox_dlm.models import (
    Contract,
    HardwareNotice,
    Provider,
    SoftwareVersion,
    ValidatedSoftware,
)


class DcimFixtureMixin:
    """Shared DCIM objects most lifecycle model tests need."""

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name="Cisco", slug="cisco")
        cls.device_type = DeviceType.objects.create(
            manufacturer=cls.manufacturer, model="Catalyst 9300", slug="cat9300"
        )
        cls.platform = Platform.objects.create(name="IOS-XE", slug="ios-xe")
        cls.role = DeviceRole.objects.create(name="Access Switch", slug="access-switch")
        cls.site = Site.objects.create(name="HQ", slug="hq")
        cls.device = Device.objects.create(
            name="sw01",
            device_type=cls.device_type,
            role=cls.role,
            site=cls.site,
            platform=cls.platform,
        )


class HardwareNoticeTestCase(DcimFixtureMixin, TestCase):
    def test_requires_exactly_one_target(self):
        notice = HardwareNotice(end_of_support=timezone.localdate())
        with self.assertRaises(ValidationError):
            notice.full_clean()

    def test_valid_with_device_type_only(self):
        notice = HardwareNotice(device_type=self.device_type, end_of_support=timezone.localdate())
        notice.full_clean()  # should not raise

    def test_end_of_support_passed(self):
        past = HardwareNotice.objects.create(
            device_type=self.device_type,
            end_of_support=timezone.localdate() - datetime.timedelta(days=1),
        )
        self.assertTrue(past.end_of_support_passed)


class ContractTestCase(DcimFixtureMixin, TestCase):
    def test_end_before_start_rejected(self):
        provider = Provider.objects.create(name="Acme Support")
        contract = Contract(
            provider=provider,
            name="Gold Support",
            start_date=timezone.localdate(),
            end_date=timezone.localdate() - datetime.timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_expired_property(self):
        provider = Provider.objects.create(name="Acme Support")
        contract = Contract.objects.create(
            provider=provider,
            name="Gold Support",
            end_date=timezone.localdate() - datetime.timedelta(days=1),
        )
        self.assertTrue(contract.expired)

    def test_covers_device_empty_scope_covers_nothing(self):
        """Unlike ValidatedSoftware, an unscoped Contract covers no devices."""
        provider = Provider.objects.create(name="Acme Support")
        contract = Contract.objects.create(provider=provider, name="Gold Support")
        self.assertFalse(contract.covers_device(self.device))

    def test_covers_device_via_platform_scope(self):
        provider = Provider.objects.create(name="Acme Support")
        contract = Contract.objects.create(provider=provider, name="Gold Support")
        contract.platforms.set([self.platform])
        self.assertTrue(contract.covers_device(self.device))


class ValidatedSoftwareTestCase(DcimFixtureMixin, TestCase):
    def test_covers_device_with_no_scope_applies_to_all(self):
        version = SoftwareVersion.objects.create(platform=self.platform, version="17.9.1")
        rule = ValidatedSoftware.objects.create(
            software_version=version, start=timezone.localdate()
        )
        self.assertTrue(rule.covers_device(self.device))

    def test_covers_device_respects_device_type_scope(self):
        version = SoftwareVersion.objects.create(platform=self.platform, version="17.9.1")
        other_type = DeviceType.objects.create(
            manufacturer=self.manufacturer, model="Catalyst 9200", slug="cat9200"
        )
        rule = ValidatedSoftware.objects.create(
            software_version=version, start=timezone.localdate()
        )
        rule.device_types.set([other_type])
        self.assertFalse(rule.covers_device(self.device))

    def test_valid_now_respects_date_range(self):
        version = SoftwareVersion.objects.create(platform=self.platform, version="17.9.1")
        future_rule = ValidatedSoftware.objects.create(
            software_version=version,
            start=timezone.localdate() + datetime.timedelta(days=30),
        )
        self.assertFalse(future_rule.valid_now)
