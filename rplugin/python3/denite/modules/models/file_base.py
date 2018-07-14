import os
import inflection


class FileBase:
    def __init__(self, filepath):
        self.filepath = os.path.normpath(filepath)

    def to_filename(self, root_path):
        filepath = self.remove_base_directory(self.filepath, root_path)
        return filepath
