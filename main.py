
import threading
from core import OS
from gui.main_frame import MainFrame


os = OS()
os.prepare_processes()
os_thread = threading.Thread(target=os.run)
if __name__ == "__main__":
    os_thread.start()
    main_frame = MainFrame()
    main_frame.run()
