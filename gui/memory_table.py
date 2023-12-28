import tkinter as tk


class MemoryTable():
    def __init__(self, root, num_pages):
        self.root = root
        self.root.title("OS 模拟器")

        # Create a canvas to draw the memory pages
        self.canvas = tk.Canvas(root, width=800, height=50)

        # Create a list to store references to the page rectangles
        self.page_rectangles = []

        # Create memory pages
        self.num_pages = num_pages
        self.page_size = 20  # Size of each memory page
        self.create_memory_pages()

    def create_memory_pages(self):
        # Calculate the width of each memory page rectangle
        page_width = 800 // self.num_pages

        # Create memory page rectangles and store references
        for i in range(self.num_pages):
            x1 = i * page_width
            x2 = (i + 1) * page_width
            y1 = 0
            y2 = 0 + 40
            rectangle = self.canvas.create_rectangle(
                x1, y1, x2, y2, fill="white", outline="black")
            self.page_rectangles.append(rectangle)

    def update_page_status(self, page_index, is_allocated):
        # Update the fill color of the specified page rectangle
        color = "green" if is_allocated else "white"
        self.canvas.itemconfig(self.page_rectangles[page_index], fill=color)

    def rand_allocate_page(self):
        # Simulate page allocation logic here
        # For example, randomly allocate a page
        import random
        page_index = random.randint(0, self.num_pages - 1)
        self.update_page_status(page_index, True)

    def update_data(self):
        from core import OS

        os = OS()
        usage = os.memory_manager.get_colored_list()
        for item in enumerate(usage):
            # is_allocated = item[1] == "Occupied"
            # self.update_page_status(item[0], is_allocated)
            self.canvas.itemconfig(self.page_rectangles[item[0]], fill=item[1])

    def get_widgets(self):
        return self.canvas
