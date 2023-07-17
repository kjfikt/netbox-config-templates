class DeviceUp(Script):
    #optional variables in UI here!
    device = StringVar(
        description="Device to update"
    )

    class Meta:
        name = "Device up"
        description = "Device is rigged up"

    def run(self, data, commit):
        now = datetime.datetime.now()
        device = Device.objects.get(serial=data['device'])
        device.status = 'active'
        device.save()
