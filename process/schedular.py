import asyncio
import threading
from time import sleep
from tkinter import messagebox
from typing import List
from gui.main_frame import MainFrame

from process.process import Process


class Scheduler:
    def __init__(self):
        self.blocking_list: List[Process] = []
        self.hipri_ready_list: List[Process] = []
        self.lopri_ready_queue: List[Process] = []
        self.current_process = None

    def set_scheduling_algorithm(self, algorithm):
        self.scheduling_algorithm = algorithm

    def schedule(self):
        # 动态优先级调度算法
        # 1. 从高优先级队列中选取一个进程执行
        # 2. 如果该进程在执行过程中被阻塞，则将其放入阻塞队列
        # 3. 如果该进程在执行过程中完成，则将其放入结束队列
        # 4. 如果该进程在执行过程中没有完成，则将其放入低优先级队列
        # 5. 如果高优先级队列为空，则从低优先级队列中选取一个进程执行
        # 6. 如果低优先级队列为空，则从阻塞队列中选取一个进程执行
        # 7. 如果阻塞队列为空，则结束调度
        # 8. 如果阻塞队列不为空，则从阻塞队列中选取一个进程执行
        # 9. 如果该进程在执行过程中被阻塞，则将其放入阻塞队列
        # 10. 如果该进程在执行过程中完成，则将其放入结束队列
        # 11. 如果该进程在执行过程中没有完成，则将其放入低优先级队列
        # 12. 回到第1步

        while True:
            sleep(1)
            if len(self.hipri_ready_list) > 0:
                process = self.hipri_ready_list.pop(0)
                self.set_current_process(process)
                result = process.run_next_command()
                if result == "IO":
                    self.block_process(process)
                elif process.pc >= len(process.commands) - 1:
                    self.finish_process(process)
                elif process.has_io_next():
                    self.add_to_hipri_ready_list(process)
                else:
                    self.add_to_lopri_ready_list(process)
            elif len(self.lopri_ready_queue) > 0:
                process = self.lopri_ready_queue.pop(0)
                self.set_current_process(process)
                result = process.run_next_command()
                if result == "IO":
                    self.block_process(process)
                if process.pc >= len(process.commands) - 1:
                    self.finish_process(process)
                elif process.has_io_next():
                    self.add_to_hipri_ready_list(process)
                else:
                    self.add_to_lopri_ready_list(process)
            elif len(self.blocking_list) > 0:
                process = self.blocking_list.pop(0)
                self.set_current_process(process)
                result = process.run_next_command()
                if result == "IO":
                    self.block_process(process)
                if process.pc >= len(process.commands) - 1:
                    self.finish_process(process)
                elif process.has_io_next():
                    self.add_to_hipri_ready_list(process)
                else:
                    self.add_to_lopri_ready_list(process)
            else:
                break
            pass

        # clear all processes
        self.hipri_ready_list = []
        self.lopri_ready_queue = []
        self.blocking_list = []

        print("DONE")
        messagebox.showinfo('提示', '全部进程结束，点击确定退出')
        mainf = MainFrame()
        mainf.suicide()

    def block_process(self, process: Process):
        self.blocking_list.append(process)

        def unblock_afterwards():
            sleep(6)
            self.wakeup_process(process)
        threading.Thread(target=unblock_afterwards).start()

    def wakeup_process(self, process: Process):
        # remove that pid from blocking list
        self.blocking_list = [
            p for p in self.blocking_list if p.pid != process.pid]
        if process.pc >= len(process.commands) - 1:
            self.finish_process(process)
        if process.has_io_next():
            self.add_to_hipri_ready_list(process)
        else:
            self.add_to_lopri_ready_list(process)

    def add_to_hipri_ready_list(self, process: Process):
        # make sure it is not in other lists
        self.lopri_ready_queue = [
            p for p in self.lopri_ready_queue if p.pid != process.pid]
        self.blocking_list = [
            p for p in self.blocking_list if p.pid != process.pid]
        self.hipri_ready_list.append(process)

    def add_to_lopri_ready_list(self, process: Process):
        # make sure it is not in other lists
        self.hipri_ready_list = [
            p for p in self.hipri_ready_list if p.pid != process.pid]
        self.blocking_list = [
            p for p in self.blocking_list if p.pid != process.pid]
        self.lopri_ready_queue.append(process)

    def set_current_process(self, process: Process):
        # filter and remove same pid process in ready list
        self.hipri_ready_list = [
            p for p in self.hipri_ready_list if p.pid != process.pid]
        self.lopri_ready_queue = [
            p for p in self.lopri_ready_queue if p.pid != process.pid]
        self.blocking_list = [
            p for p in self.blocking_list if p.pid != process.pid]
        self.current_process = process

    def finish_process(self, process: Process):
        self.current_process = None
        self.lopri_ready_queue = [
            p for p in self.lopri_ready_queue if p.pid != process.pid]
        self.hipri_ready_list = [
            p for p in self.hipri_ready_list if p.pid != process.pid]
        self.blocking_list = [
            p for p in self.blocking_list if p.pid != process.pid]
