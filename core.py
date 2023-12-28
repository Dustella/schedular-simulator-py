from typing import List
from external.device_man import DeviceManager
from external.filesystem_man import FilesystemManager
from memory.mem_manager import MemoryManager
from process.process import Process
from process.schedular import Scheduler
from context import proceses
from process.command import Command
from utils.thread_safe_singleton import SingletonMeta


class OS(metaclass=SingletonMeta):
    memory_manager = MemoryManager(24)
    device_manager = DeviceManager()
    filesystem_manager = FilesystemManager()
    schedular = Scheduler()

    def __init__(self):
        pass

    def prepare_processes(self):
        pid_set = set()
        from random import randint
        for process in proceses:
            new_pid = randint(0, 100)
            while new_pid in pid_set:
                new_pid = randint(0, 100)
            process_item = Process(process["PID"])
            instructions: List[Command] = []
            for command in process["commands"]:
                command_line = Command(command)
                command_line.set_process(process_item)

                instructions.append(command_line)
            process_item.set_commands(commands=instructions)
            process_item.set_name(process["name"])
            self.schedular.add_to_hipri_ready_list(process=process_item)

    def run(self):
        self.schedular.schedule()
