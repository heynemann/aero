#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from os.path import join

from tornado.template import BaseLoader, Template, _DEFAULT_AUTOESCAPE

class AppTemplateLoader(BaseLoader):
    def __init__(self, app, autoescape=_DEFAULT_AUTOESCAPE):
        BaseLoader.__init__(self, autoescape)
        self.app = app

    def resolve_path(self, name, parent_path=None):
        paths = []
        for application in self.app.apps:
            if not application['has_templates']:
                continue
            paths.append(application['template_path'])
            return join(application['template_path'], name)

        raise RuntimeError('Template with path %s could not be found in any of the available template paths: %s.' % ", ".join(paths))

    def _create_template(self, name):
        f = open(name, "r")
        template = Template(f.read(), name=name, loader=self)
        f.close()
        return template
