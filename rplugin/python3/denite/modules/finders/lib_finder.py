import finder_utils

from lib_file import LibFile


class LibFinder:

    GLOB_PATTERN = 'lib/**/*.rb'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        return [LibFile(filename) for filename in files]
