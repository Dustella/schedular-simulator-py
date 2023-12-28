
from tkinter import ttk


class ProcessTable:
    def __init__(self, window):
        self.window = window
        self.create_tables()
        self.init_cols()

    def create_tables(self):

        # 高优先级就绪队列
        self.hipri_ready_queue = ttk.Treeview(self.window)

#      # 低优先级就绪队列
        self.lopri_ready_queue = ttk.Treeview(self.window)

        # 阻塞队列
        self.blocking_queue = ttk.Treeview(self.window)

        self.current = ttk.Label(self.window, text="当前进程", font=("微软雅黑", 15))

    def get_current(self):
        return self.current

    def init_cols(self):
        self.hipri_ready_queue["columns"] = ("PID", "Memory", "Name")

        self.hipri_ready_queue.column("#0", width=0)
        self.hipri_ready_queue.column("PID", width=80)
        self.hipri_ready_queue.column("Memory", width=80)
        self.hipri_ready_queue.column("Name", width=80)
        self.hipri_ready_queue.heading("PID", text="PID")
        self.hipri_ready_queue.heading("Memory", text="Memory")
        self.hipri_ready_queue.heading("Name", text="Name")

        self.blocking_queue["columns"] = ("PID", "Memory", "Name")
        self.blocking_queue.column("#0", width=0)
        self.blocking_queue.column("PID", width=80)
        self.blocking_queue.column("Memory", width=80)
        self.blocking_queue.column("Name", width=80)
        self.blocking_queue.heading("PID", text="PID")
        self.blocking_queue.heading("Memory", text="Memory")
        self.blocking_queue.heading("Name", text="Name")

        self.lopri_ready_queue["columns"] = ("PID", "Memory", "Name")
        self.lopri_ready_queue.column("#0", width=0)
        self.lopri_ready_queue.column("PID", width=80)
        self.lopri_ready_queue.column("Memory", width=80)
        self.lopri_ready_queue.column("Name", width=80)
        self.lopri_ready_queue.heading("PID", text="PID")
        self.lopri_ready_queue.heading("Memory", text="Memory")
        self.lopri_ready_queue.heading("Name", text="Name")

    def update_rows(self):
        # Update the tables
        from core import OS

        os = OS()
        current_process = os.schedular.current_process
        hipri_ready_list = os.schedular.hipri_ready_list
        lopri_ready_list = os.schedular.lopri_ready_queue
        blocked_list = os.schedular.blocking_list

        self.hipri_ready_queue.delete(*self.hipri_ready_queue.get_children())
        for p in hipri_ready_list:
            row = (p.pid, p.get_mem_size(), p.name)
            self.hipri_ready_queue.insert("", "end", values=row)

        self.blocking_queue.delete(*self.blocking_queue.get_children())
        for p in blocked_list:
            row = (p.pid, p.get_mem_size(), p.name)
            self.blocking_queue.insert("", "end", values=row)

        self.lopri_ready_queue.delete(*self.lopri_ready_queue.get_children())
        for p in lopri_ready_list:
            row = (p.pid, p.get_mem_size(), p.name)
            self.lopri_ready_queue.insert("", "end", values=row)

        self.current["text"] = "当前进程: " + \
            f"PID: {current_process.pid} 进程名: {
                current_process.name}" if current_process else "当前进程: None"

    def get_widgets(self):
        return self.hipri_ready_queue, self.blocking_queue, self.lopri_ready_queue
