from typing import List

import strawberry
import strawberry_django

from . import types


@strawberry.type
class DeviceLifecycleQuery:
    provider: types.ProviderType = strawberry_django.field()
    provider_list: List[types.ProviderType] = strawberry_django.field()

    contract: types.ContractType = strawberry_django.field()
    contract_list: List[types.ContractType] = strawberry_django.field()

    hardware_notice: types.HardwareNoticeType = strawberry_django.field()
    hardware_notice_list: List[types.HardwareNoticeType] = strawberry_django.field()

    software_version: types.SoftwareVersionType = strawberry_django.field()
    software_version_list: List[types.SoftwareVersionType] = strawberry_django.field()

    software_image_file: types.SoftwareImageFileType = strawberry_django.field()
    software_image_file_list: List[types.SoftwareImageFileType] = strawberry_django.field()

    device_software: types.DeviceSoftwareType = strawberry_django.field()
    device_software_list: List[types.DeviceSoftwareType] = strawberry_django.field()

    validated_software: types.ValidatedSoftwareType = strawberry_django.field()
    validated_software_list: List[types.ValidatedSoftwareType] = strawberry_django.field()

    cve: types.CVEType = strawberry_django.field()
    cve_list: List[types.CVEType] = strawberry_django.field()

    vulnerability: types.VulnerabilityType = strawberry_django.field()
    vulnerability_list: List[types.VulnerabilityType] = strawberry_django.field()


schema = [DeviceLifecycleQuery]
