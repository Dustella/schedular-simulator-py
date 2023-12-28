

from gui.main_frame import MainFrame


class Command:

    def __init__(self, info):
        print(info)
        self.action = info["actions"]
        if "target" in info:
            self.target = info["target"]
        if "amount" in info:
            self.amount = info["amount"]
        if "size" in info:
            self.size = info["size"]

    def set_process(self, process):
        self.process = process

    def excute(self):
        from core import OS
        os = OS()
        # mainfram = MainFrame()
        # mainfram.log("wiw")

        if self.action == "malloc":
            addr = os.memory_manager.allocate(
                self.process.pid, self.target, self.size)

        if self.action == "free":

            os.memory_manager.free(self.process.pid, self.target, self.size)

        if self.action == "visit":
            os.memory_manager.visit(self.process.pid, self.target)

        if self.action == "use_device":

            os.device_manager.acquire_device(self.target)

        if self.action == "release_device":

            os.device_manager.release_device(self.target)

        if self.action == "read_file":

            os.filesystem_manager.read_file(self.process.pid, self.target)
            return "IO"

        if self.action == "write_file":

            os.filesystem_manager.write_file(self.process.pid, self.target)
            return "IO"

    def is_io(self):
        return self.action == "write_file" or self.action == "read_file"


#     {
#         "name": "P1",
#         "PID": 1,
#         "commands": [
#             {
#                 "actions": "malloc",
#                 "size": 1,
#                 "target": "var1"
#             },
#             {
#                 "receive": "channel1",
#                 "size": 10
#             },
#             {
#                 "actions": "free",
#                 "target": "var1"
#             },
#             {
#                 "actions": "malloc",
#                 "size": 1,
#                 "target": "var2"
#             },
#             {
#                 "actions": "free",
#                 "target": "var2"
#             },
#             {
#                 "actions": "malloc",
#                 "size": 1,
#                 "target": "var3"
#             },
#             {
#                 "actions": "free",
#                 "target": "var3"
#             }
#         ]
#     },
#     {
#         "name": "P2",
#         "PID": 2,
#         "commands": [
#             {
#                 "actions": "create_channel",
#                 "target": "channel1"
#             },
#             {
#                 "actions": "send",
#                 "target": "channel1",
#                 "amount": 10
#             },
#             {
#                 "actions": "use_device",
#                 "target": "device1"
#             },
#             {
#                 "actions": "release_device",
#                 "target": "device1"
#             },
#             {
#                 "actions": "use_device",
#                 "target": "printer1"
#             },
#             {
#                 "actions": "release_device",
#                 "target": "printer1"
#             },
#             {
#                 "actions": "use_device",
#                 "target": "printer2"
#             },
#             {
#                 "actions": "release_device",
#                 "target": "printer2"
#             }
#         ]
#     },
#     {
#         "name": "P3",
#         "PID": 3,
#         "commands": [
#             {
#                 "actions": "read_file",
#                 "target": "file1"
#             },
#             {
#                 "actions": "write_file",
#                 "target": "file1"
#             },
#             {
#                 "actions": "receive",
#                 "target": "channel1",
#                 "amount": 10
#             },
#             {
#                 "actions": "read_file",
#                 "target": "file2"
#             },
#             {
#                 "actions": "write_file",
#                 "target": "file2"
#             },
#             {
#                 "actions": "read_file",
#                 "target": "file3"
#             },
#             {
#                 "actions": "write_file",
#                 "target": "file3"
#             }

#         ]
#     }
# ]
