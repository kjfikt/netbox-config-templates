from django.utils.text import slugify

from dcim.choices import *
from dcim.models import Cable, Device, DeviceRole, DeviceType, Platform, Rack, RackRole, Site
from dcim.models.device_components import FrontPort, Interface, RearPort

from ipam.choices import *
from ipam.models import Aggregate, Prefix, IPAddress, Role, VLAN
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site

from extras.scripts import *
import datetime


class DeviceUp(Script):
    #optional variables in UI here!
    device_sn = StringVar(
        description="Serial number for device to update"
    )

    class Meta:
        name = "Device up"
        description = "Device is rigged up"

    def run(self, data, commit):
        device = Device.objects.get(serial=data['device_sn'])
        device.status = 'active'
        device.save()
