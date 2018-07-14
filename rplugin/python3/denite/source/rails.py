# -*- coding: utf-8 -*-

from denite import util
from .base import Base

import os
import site

# Add external modules
path_to_parent_dir = os.path.abspath(os.path.dirname(__file__) + '/../')
path_to_modules = os.path.join(path_to_parent_dir, 'modules')
site.addsitedir(path_to_modules)
site.addsitedir(os.path.join(path_to_modules, 'inflection'))
site.addsitedir(os.path.join(path_to_modules, 'finders'))
site.addsitedir(os.path.join(path_to_modules, 'models'))

from dwim_finder import DwimFinder # noqa
from general_finder import GeneralFinder # noqa

class Source(Base):

    GLOB_ROOT_PATHS = {
        'model': { 'path': 'app/models', 'extension': 'rb' },
        'controller': { 'path': 'app/controllers', 'extension': 'rb' },
        'helper': { 'path': 'app/helpers', 'extension': 'rb' },
        'view': { 'path': 'app/views', 'extension': 'html*' },
        'test': { 'path': 'test', 'extension': 'rb' },
        'spec': { 'path': 'spec', 'extension': 'rb' },
        'config': { 'path': 'config', 'extension': 'rb' },
        'lib': { 'path': 'lib', 'extension': 'rb' },
        'graphql': { 'path': 'app/graphql', 'extension': 'rb' },
        'javascript': { 'path': 'app/javascript', 'extension': 'js*' },
        'service': { 'path': 'app/services', 'extension': 'rb' },
    }

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'rails'
        self.kind = 'file'

    def on_init(self, context):
        try:
            context['__target'] = context['args'][0]
        except IndexError:
            raise NameError('target must be provided')

        cbname = self.vim.current.buffer.name
        context['__cbname'] = cbname
        context['__root_path'] = util.path2project(self.vim, cbname, context.get('root_markers', ''))

    def highlight(self):
        # TODO syntax does not work as expected
        self.vim.command('syntax region deniteSource_railsConstant start=+^+ end=+^.\{-}\s+')
        self.vim.command('highlight link deniteSource_railsConstant Statement')
        self.vim.command('syntax match deniteSource_railsSeparator /::/ containedin=deniteSource_railsConstant')
        self.vim.command('highlight link deniteSource_railsSeparator Identifier')
        self.vim.command('syntax region deniteSource_railsPath start=+(+ end=+)+')
        self.vim.command('highlight link deniteSource_railsPath Statement')
        self.vim.command('syntax match deniteSource_railsController /Controller:/')
        self.vim.command('highlight link deniteSource_railsController Function')
        self.vim.command('syntax match deniteSource_railsModel /Model:/')
        self.vim.command('highlight link deniteSource_railsModel String')
        self.vim.command('syntax match deniteSource_railsHelper /Helper:/')
        self.vim.command('highlight link deniteSource_railsHelper Type')
        self.vim.command('syntax match deniteSource_railsView /View:/')
        self.vim.command('highlight link deniteSource_railsView Statement')
        self.vim.command('syntax match deniteSource_railsTest /Test:/')
        self.vim.command('highlight link deniteSource_railsTest Number')
        self.vim.command('syntax match deniteSource_railsSpec /Spec:/')
        self.vim.command('highlight link deniteSource_railsSpec Number')
        self.vim.command('syntax match deniteSource_railsConfig /Config:/')
        self.vim.command('highlight link deniteSource_railsConfig Statement')
        self.vim.command('syntax match deniteSource_railsLib /Lib:/')
        self.vim.command('highlight link deniteSource_railsLib Statement')

    def gather_candidates(self, context):
        file_list = self._find_files(context)
        if file_list is not None:
            return [self._convert(context, x) for x in file_list]
        else:
            return []

    def _find_files(self, context):
        target = context['__target']

        if target == 'dwim':
            finder_class = DwimFinder
            return DwimFinder(context).find_files()
        elif self.GLOB_ROOT_PATHS[target]:
            glob_root_path = self.GLOB_ROOT_PATHS[target]
            return GeneralFinder(context).find_files(glob_root_path['path'], glob_root_path['extension'])
        else:
            msg = '{0} is not valid denite-rails target'.format(target)
            raise NameError(msg)

    def _convert(self, context, file_object):
        result_dict = {
            'word': file_object.to_filename(context['__root_path']),
            'action__path': file_object.filepath
        }

        return result_dict
