from time import time


class MemoryManager:
    def __init__(self, total_memory_pages=24):
        self.total_memory_pages = total_memory_pages

        # 列表长度为内存总页数，每个元素为进程pid，None表示空闲
        self.memory = [None] * total_memory_pages

        # 映射关系： pid -> virtual page index in program
        self.vitual_page = {}

        # 映射关系： pid -> virtual page index in program -> real address on memory
        self.page_mapping = {}

        # 映射关系： pid -> real page index on memory -> last visit time
        self.last_visit_mapping = {}

        self.swaped_index = set()

    def allocate(self, pid, addr, need_size):
        if pid not in self.page_mapping:
            self.page_mapping[pid] = {}
        if pid not in self.last_visit_mapping:
            self.last_visit_mapping[pid] = {}

        for i in range(need_size):
            page_index = self.get_free_page_index()
            if page_index == -1:
                swap_page_index = self.get_least_unused_page()
                self.swap(swap_page_index, pid, addr + i)
            self.memory[page_index] = pid
            self.last_visit_mapping[pid][page_index] = time()
            self.page_mapping[pid][addr + i] = f"R{page_index}"

    def free(self, pid, virtual_addr, free_size):
        if pid not in self.page_mapping:
            return
        if pid not in self.last_visit_mapping:
            return

        for i in range(free_size):
            real_page_index = self.page_mapping[pid][virtual_addr + i]
            if real_page_index == "V":
                continue
            if real_page_index is None:
                continue
            int_index = real_page_index[1:]
            self.memory[int(int_index)] = None
            self.last_visit_mapping[pid][real_page_index] = None
            self.page_mapping[pid][virtual_addr + i] = "Freed"

    def visit(self, pid, addr):
        if pid not in self.page_mapping:
            return False
        if addr not in self.page_mapping[pid]:
            return False
        if pid not in self.last_visit_mapping:
            self.last_visit_mapping[pid] = {}

        real_page_index = self.page_mapping[pid][addr]
        flag = real_page_index[0]
        if flag == "R":
            real_page_index = int(real_page_index[1:])
            self.last_visit_mapping[pid][real_page_index] = time()
            return True
        else:
            # trigger swap
            # swap page index
            real_page_index = int(real_page_index[1:])
            swap_page_index = self.get_least_unused_page()
            self.swap(swap_page_index, pid, addr)
            self.memory[real_page_index] = pid
            self.last_visit_mapping[pid][real_page_index] = time()
            return False

    def swap(self, target_page_index, pid, addr):
        # take content from the page index
        # and put it into the disk
        pid = self.memory[target_page_index]
        # addr = self.page_mapping[pid].index(f"R{page_index}")
        # dict cannot index, use .items()
        for page_index, real_addr in self.page_mapping[pid].items():
            if real_addr == f"R{target_page_index}":
                addr = page_index
                break

        self.page_mapping[pid][target_page_index] = "V"
        if pid not in self.vitual_page:
            self.vitual_page[pid] = []
        self.vitual_page[pid].append(str(addr))

        self.memory[target_page_index] = None
        self.page_mapping[pid][addr] = None

        self.swaped_index.add(target_page_index)

    def get_least_unused_page(self):
        # to get least unused memory page
        # we need to get the least recently used page
        # and the page that has not been used
        least_recently_used_page = None
        least_recently_used_time = time()
        for pid in self.last_visit_mapping:
            for page_index in self.last_visit_mapping[pid]:
                this_last_visit = self.last_visit_mapping[pid][page_index] if self.last_visit_mapping[pid][page_index] is not None else time(
                )
                if this_last_visit < least_recently_used_time:
                    least_recently_used_page = page_index
                    least_recently_used_time = this_last_visit
        return least_recently_used_page

    def get_free_page_index(self):
        for index, page in enumerate(self.memory):
            if page is None:
                return index
        return -1

    def get_colored_list(self):
        res = []
        for index, item in enumerate(self.memory):
            if item is None:
                res.append("white")
            else:
                color = "blue" if index in self.swaped_index else "green"
                res.append(color)
        return res

    def get_page_status(self):
        # return a list of (pid, virtual_addr, real_addr)
        res = []
        for pid in self.page_mapping:
            for addr in self.page_mapping[pid]:
                if self.page_mapping[pid][addr] != "V":
                    res.append((pid, addr, self.page_mapping[pid][addr]))
                else:
                    res.append((pid, addr, "Swaped"))
        return res
