import time
from typing import List
from context import get_all_files


class FilesystemManager:
    def __init__(self):
        self.full_filelist = get_all_files()
        self.files = {}

    def read_file(self, process_id, file_path):
        if file_path in self.files:
            if self.files[file_path] == process_id:
                print(f"Process {process_id} is reading file {file_path}")
            else:
                print(f"File {file_path} is already being used by process {
                      self.files[file_path]}")
        else:
            self.files[file_path] = process_id
            print(f"Process {process_id} is reading file {file_path}")
            time.sleep(5)
            self.release_file(process_id, file_path)

    def write_file(self, process_id, file_path):
        if file_path in self.files:
            if self.files[file_path] == process_id:
                print(f"Process {process_id} is writing to file {file_path}")
            else:
                print(f"File {file_path} is already being used by process {
                      self.files[file_path]}")
        else:
            self.files[file_path] = process_id
            print(f"Process {process_id} is writing to file {file_path}")
            time.sleep(5)
            self.release_file(process_id, file_path)

    def release_file(self, process_id, file_path):
        if file_path in self.files:
            if self.files[file_path] == process_id:
                del self.files[file_path]
                print(f"Process {process_id} released file {file_path}")
            else:
                print(f"Process {process_id} cannot release file {
                      file_path} as it is being used by process {self.files[file_path]}")
        else:
            print(f"File {file_path} is not being used by any process")

    def get_status(self) -> List[str]:
        result = []
        for file in self.full_filelist:
            if file in self.files:
                message = f"File {file} Used, by process {
                    self.files[file]}"
            else:
                message = f"File {file} Free"
            result.append(message)
        return result
