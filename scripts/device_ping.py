

from django.utils.text import slugify

from dcim.choices import *
from dcim.models import Cable, Device, DeviceRole, DeviceType, Platform, Rack, RackRole, Site
from dcim.models.device_components import FrontPort, Interface, RearPort

from ipam.choices import *
from ipam.models import Aggregate, Prefix, IPAddress, Role, VLAN
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site

from extras.scripts import *
import datetime


class DevicePing(Script):
    #optional variables in UI here!
    device = StringVar(
        description="Device to update"
    )
    firmware_version = StringVar(
        description="Firmware version"
    )
    config_timestamp = StringVar(
        description="Configuration timestamp"
    )

    class Meta:
        name = "Device ping"
        description = "Script to update device"

    def run(self, data, commit):
        now = datetime.datetime.now()
        device = Device.objects.get(serial=data['device'])
        device.custom_field_data["firmware_version"] = data["firmware_version"]
        device.custom_field_data["ping_timestamp"] = f"{now.date()}"
        device.custom_field_data["ping_clock"] = now.time()
        device.custom_field_data["config_timestamp"] = data["config_timestamp"]
        device.save()
        self.log_info(f"Data saved for device '{device}'")