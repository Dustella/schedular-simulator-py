from time import sleep
from process import command
from typing import List


class Process:
    def __init__(self, pid):
        self.pid = pid
        self.pc = 0
        self.memory_mapping = {}

    def set_name(self, name):
        self.name = name

    def set_commands(self, commands: List[command.Command]):
        self.commands = commands

    def record_memory_mapping(self, var, start_page, size):
        self.memory_mapping[var] = (start_page, size)

    def get_mem_size(self):
        from core import OS
        os = OS()
        men_c = os.memory_manager
        if self.pid not in men_c.page_mapping:
            return 0
        mapper = men_c.page_mapping[self.pid]
        return len(mapper.items())

    def run_to_die(self):
        while self.pc < len(self.commands):
            command = self.commands[self.pc]
            if command.is_io():
                command.excute()
                return "IO"
            command.excute()
            sleep(2)
            self.pc += 1

        return "Done"

    def run_next_command(self):
        command = self.commands[self.pc]
        if command.is_io():
            command.excute()
            if self.pc >= len(self.commands) - 1:
                return "Done"
            self.pc += 1
            return "IO"
        command.excute()
        self.pc += 1
        return "Done"

    def has_io_next(self):
        # returns if there is IO in the following commands
        for i in range(self.pc, len(self.commands)):
            if self.commands[i].is_io():
                return True

        return False
