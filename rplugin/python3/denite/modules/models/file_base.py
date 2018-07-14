import os
import inflection


class FileBase:
    def __init__(self, filepath):
        self.filepath = os.path.normpath(filepath)

    def to_filename(self, root_path):
        filepath = self.remove_base_directory(self.filename_without_extension(), root_path)
        return filepath

    def filename_without_extension(self):
        return os.path.splitext(self.filepath)[0]
