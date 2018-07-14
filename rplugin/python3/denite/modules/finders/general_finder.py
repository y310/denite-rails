import finder_utils

from general_file import GeneralFile


class GeneralFinder:

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self, glob_root_path, extension='rb'):
        files = finder_utils.glob_project(self.root_path, glob_root_path + '/**/*.' + extension)
        return [GeneralFile(filename, glob_root_path) for filename in files]
