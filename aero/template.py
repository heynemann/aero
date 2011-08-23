#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from os.path import join, exists

from tornado.template import BaseLoader, Template, _DEFAULT_AUTOESCAPE

class AppTemplateLoader(BaseLoader):
    def __init__(self, app, root_path=None, autoescape=_DEFAULT_AUTOESCAPE):
        BaseLoader.__init__(self, autoescape)
        self.app = app
        self.root_path = root_path

    def resolve_path(self, name, parent_path=None):
        paths = []

        if self.root_path:
            paths.append(self.root_path)
            template_path = join(self.root_path.rstrip('/'), name.lstrip('/'))
            if exists(template_path):
                return template_path

        for application in self.app.apps:
            if not application['has_templates']:
                continue
            paths.append(application['template_path'])
            template_path = join(application['template_path'].rstrip('/'), name.lstrip('/'))
            if exists(template_path):
                return template_path

        raise RuntimeError('Template with path %s could not be found in any of the available template paths: %s.' % ", ".join(paths))

    def _create_template(self, name):
        f = open(name, "r")
        template = Template(f.read(), name=name, loader=self)
        f.close()
        return template
