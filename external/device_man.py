from context import get_all_devices


class DeviceManager:
    def __init__(self):
        self.devices = {}
        all_set = get_all_devices()
        self.all_devices = all_set

    def use_device(self, name):
        pass

    def acquire_device(self, device_id):
        if device_id in self.devices and self.devices[device_id]:
            print(f"Device {device_id} is already acquired.")
        else:
            self.devices[device_id] = True
            print(f"Device {device_id} acquired.")

    def release_device(self, device_id):
        if device_id in self.devices and self.devices[device_id]:
            self.devices[device_id] = False
            print(f"Device {device_id} released.")
        else:
            print(f"Device {device_id} is not currently acquired.")

    def add_device(self, device_id):
        if device_id in self.devices:
            print(f"Device {device_id} already exists.")
        else:
            self.devices[device_id] = False
            print(f"Device {device_id} added.")

    def query_device_usage(self):
        return self.devices

    def get_status(self):
        res = []
        for i in self.all_devices:
            if i in self.devices and self.devices[i]:
                res.append(f"{i} is acquired")
            else:
                res.append(f"{i} is not acquired")
        return res
