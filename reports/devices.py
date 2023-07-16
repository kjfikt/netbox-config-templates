from dcim.choices import DeviceStatusChoices
from dcim.models import Device
from extras.reports import Report
from datetime import datetime, timedelta
import pytz


class DeviceReconfigureReport(Report):
    description = "Devices that needs new configuration"

    def test_power_connections(self):
        # Check that every active device has at least two connected power supplies.
        for device in Device.objects.all():
            if (
                device.status == DeviceStatusChoices.STATUS_DECOMMISSIONING
                or device.status == DeviceStatusChoices.STATUS_INVENTORY
            ):
                self.log_success(
                    device,
                    "Ignore status '{}' for '{}'".format(device.status, device.id),
                )
                continue
            if (
                device.device_role.name == "Switch"
                or device.device_role.name == "Router - Uplink"
            ):
                self.log_success(
                    device,
                    "Ignore role '{}' for device '{}'".format(
                        device.device_role.name, device.id
                    ),
                )
                continue
            if device.device_type.id == 20:
                self.log_success(
                    device,
                    "Ignore device type 'Mikrotik Wireless Wire Cube Pro' for device '{}'".format(
                        device.id
                    ),
                )
                continue
            if device.device_type.id == 3:
                self.log_success(
                    device,
                    "Ignore device type 'Mikrotik wAP 60G AP' for device '{}'".format(
                        device.id
                    ),
                )
                continue
            if device.device_type.id == 2:
                self.log_success(
                    device,
                    "Ignore device type 'Mikrotik RB1100x4' for device '{}'".format(
                        device.id
                    ),
                )
                continue

            last_updated = device.last_updated
            ping_timestamp_str = device.custom_field_data["ping_timestamp"]
            ping_clock_str = device.custom_field_data["ping_clock"]
            if ping_timestamp_str is None or ping_clock_str is None:
                self.log_warning(
                    device, "Device '{}' has no ping data".format(device.id)
                )
                continue

            try:
                ping_timestamp_unaware = datetime.strptime(
                    ping_timestamp_str, "%Y-%m-%d"
                )
                ping_timestamp = pytz.utc.localize(ping_timestamp_unaware)
                ping_clock = datetime.strptime(ping_clock_str, "%H:%M:%S.%f").time()
            except:
                self.log_warning(
                    device,
                    "Could not convert ping data '{} {}' for device '{}'".format(
                        ping_timestamp_str, ping_clock_str, device.id
                    ),
                )
                continue

            ping = ping_timestamp + timedelta(
                hours=ping_clock.hour,
                minutes=ping_clock.minute,
                seconds=ping_clock.second + 2,
            )
            try:
                if last_updated > ping:
                    self.log_warning(
                        device,
                        "Device configuration has been changed after last reset: {} > {}".format(
                            last_updated, ping
                        ),
                    )
                else:
                    self.log_success(device, "Device '{}' OK".format(device.id))
            except Exception as inst:
                self.log_warning(
                    device,
                    "Could not evaluate dates for device '{}'. Last updated '{}', ping date '{}'. {} ".format(
                        device.id, last_updated, ping_timestamp_str, inst
                    ),
                )
                continue

    # def test_config_timestamp(self):
    #     # Check that every active device has at least two connected power supplies.
    #     for device in Device.objects.all():
    #         if (
    #             device.status == DeviceStatusChoices.STATUS_DECOMMISSIONING
    #             or device.status == DeviceStatusChoices.STATUS_INVENTORY
    #         ):
    #             self.log_success(
    #                 device,
    #                 "Ignore status '{}' for device '{}'".format(
    #                     device.status, device.id
    #                 ),
    #             )
    #             continue
    #         if (
    #             device.device_role.name == "Switch"
    #             or device.device_role.name == "Router - Uplink"
    #         ):
    #             self.log_success(
    #                 device,
    #                 "Ignore role '{}' for '{}'".format(
    #                     device.device_role.name, device.id
    #                 ),
    #             )
    #             continue
    #         last_updated = device.last_updated
    #         config_timestamp_string = device.custom_field_data["config_timestamp"]

    #         if config_timestamp_string is None:
    #             self.log_warning(
    #                 device, "Missing config timestamp for device '{}'".format(device.id)
    #             )
    #             continue

    #         try:
    #             config_timestamp_unaware = datetime.fromisoformat(
    #                 config_timestamp_string[:-1]
    #             )
    #             config_timestamp = pytz.utc.localize(config_timestamp_unaware)
    #         except Exception as ex:
    #             self.log_warning(
    #                 device,
    #                 "Could not convert config timestamp '{}' for device '{}'. {}".format(
    #                     config_timestamp_string, device.id, ex
    #                 ),
    #             )
    #             continue

    #         try:
    #             if last_updated > config_timestamp:
    #                 self.log_warning(
    #                     device,
    #                     "Device configuration has been changed after last reset: {} > {}".format(
    #                         last_updated, config_timestamp
    #                     ),
    #                 )
    #             else:
    #                 self.log_success(device, "Device OK '{}'".format(device.id))
    #         except Exception as inst:
    #             self.log_failure(
    #                 device,
    #                 "Could not evaluate dates. Last updated '{}', ping date '{}'. {} ".format(
    #                     last_updated, config_timestamp_string, inst
    #                 ),
    #             )
    #             continue
