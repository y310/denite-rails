import re
import os

from file_base import FileBase


class GeneralFile(FileBase):
    def __init__(self, filepath, glob_root_path):
        super().__init__(filepath)
        self.glob_root_path = glob_root_path

    def remove_base_directory(self, filename, root_path):
        return re.sub(os.path.join(root_path, self.glob_root_path + '/'), '', filename)
