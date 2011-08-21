#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from os.path import abspath, join, dirname, exists

import tornado.web

from aero.template import AppTemplateLoader

class AeroApp(tornado.web.Application):

    def __init__(self, apps):
        handlers = []
        self.apps = []

        for app_module_name in apps:
            self.apps.append(self.__load_app(app_module_name))

        for app in self.apps:
            for url in app['urls']:
                handlers.append(url)

        settings = {
            "template_loader": AppTemplateLoader(self)
            #"cookie_secret": "QmVybmFyZG8gSGV5bmVtYW5uIE5hc2NlbnRlcyBkYSBTaWx2YQ==",
            #"login_url": "/login",
            #"template_path": join(dirname(__file__), "templates"),
            #"static_path": join(dirname(__file__), "static"),
        }

        super(AeroApp, self).__init__(handlers, **settings)

    def __load_app(self, app_name):
        try:
            module = reduce(getattr, app_name.split('.')[1:], __import__(app_name))
        except ImportError, err:
            print "Could not import app %s! Error:" % app_name
            raise err

        urls = []
        urls_app_name = '%s.urls' % app_name
        urls_module = reduce(getattr, urls_app_name.split('.')[1:], __import__(urls_app_name))

        if hasattr(urls_module, 'urls'):
            for url in urls_module.urls:
                urls.append(url)

        template_path = abspath(join(dirname(module.__file__), 'templates'))
        has_templates = exists(template_path)

        return {
            'name': app_name,
            'module': module,
            'urls_module': urls,
            'urls': urls,
            'has_templates': has_templates,
            'template_path': template_path
        }
