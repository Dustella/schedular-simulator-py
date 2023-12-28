# Create the lists
import tkinter as tk
from tkinter import ttk


class DevPannel:
    def __init__(self, window) -> None:

        self.window = window
        self.file_lists = tk.Listbox(self.window)

        self.device_list = tk.Listbox(self.window)

        page_table = ttk.Treeview(self.window)

        page_table["columns"] = ("PID", "Virt Addr", "Real Addr")
        page_table.column("#0", width=0)
        page_table.column("PID", width=80)
        page_table.column("Virt Addr", width=80)
        page_table.column("Real Addr", width=80)
        page_table.heading("PID", text="PID")
        page_table.heading("Virt Addr", text="Virt Addr")
        page_table.heading("Real Addr", text="Real Addr")

        self.page_table = page_table

    def update_rows(self):
        from core import OS

        os = OS()
        file_list_data = os.filesystem_manager.get_status()
        self.file_lists.delete(0, tk.END)
        for item in file_list_data:
            self.file_lists.insert(tk.END, item)

        page_data = os.memory_manager.get_page_status()
        self.page_table.delete(*self.page_table.get_children())
        for item in page_data:
            self.page_table.insert("", tk.END, values=item)

        device_data = os.device_manager.get_status()
        self.device_list.delete(0, tk.END)
        for item in device_data:
            self.device_list.insert(tk.END, item)

    def get_widgets(self):
        return self.file_lists, self.device_list, self.page_table
