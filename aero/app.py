#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from os.path import abspath, join, dirname, exists

import tornado.web
from cyrusbus import Bus

from aero.template import AppTemplateLoader
from aero.static import AeroStaticFileHandler

class AeroApp(tornado.web.Application):

    def __init__(self, handlers=[], **settings):
        handlers = list(handlers)

        self.bus = Bus()
        self.apps = []
        if not settings:
            settings = {}

        if 'apps' in settings:
            apps = settings['apps']

            for app_module_name in apps:
                self.apps.append(self.__load_app(app_module_name))

            for app in self.apps:
                for url in app['urls']:
                    handlers.append(url)

            if 'template_path' in settings:
                self.loader = AppTemplateLoader(self, settings['template_path'])
            else:
                self.loader = AppTemplateLoader(self)

            settings['template_loader'] = self.loader

        handlers.append((r"/static/(.*)", AeroStaticFileHandler, {
            "path": "static_path" in settings and settings['static_path'] or None,
            "apps": self.apps
        }))
        if 'static_path' in settings:
            del settings['static_path']

        #"cookie_secret": "QmVybmFyZG8gSGV5bmVtYW5uIE5hc2NlbnRlcyBkYSBTaWx2YQ==",
        #"login_url": "/login",
        #"template_path": join(dirname(__file__), "templates"),
        #"static_path": join(dirname(__file__), "static"),

        for app in self.apps:
            if not app['has_listeners']: continue

            if hasattr(app['listeners'], 'listen'):
                app['listeners'].listen(self)

        self.publish('app_started', app=self)
        super(AeroApp, self).__init__(handlers, **settings)

    def subscribe(self, key, callback, force=False):
        return self.bus.subscribe(key, callback, force)

    def publish(self, key, *args, **kwargs):
        return self.bus.publish(key, *args, **kwargs)

    def __load_app(self, app_name):
        try:
            module = reduce(getattr, app_name.split('.')[1:], __import__(app_name))
        except ImportError, err:
            print "Could not import app %s! Error:" % app_name
            raise err

        app_path = abspath(dirname(module.__file__))

        urls = []
        urls_module = None

        if exists(join(app_path.rstrip('/'), 'urls.py')):
            urls_app_name = '%s.urls' % app_name
            urls_module = reduce(getattr, urls_app_name.split('.')[1:], __import__(urls_app_name))

            if hasattr(urls_module, 'urls'):
                for url in urls_module.urls:
                    urls.append(url)

        listeners_module = None
        if exists(join(app_path.rstrip('/'), 'listeners.py')):
            listeners_module_name = '%s.listeners' % app_name
            listeners_module = reduce(getattr, listeners_module_name.split('.')[1:], __import__(listeners_module_name))

        template_path = abspath(join(dirname(module.__file__), 'templates'))
        has_templates = exists(template_path)

        static_path = abspath(join(dirname(module.__file__), 'static'))
        has_static = exists(static_path)

        return {
            'name': app_name,
            'module': module,
            'path': app_path,
            'urls_module': urls_module,
            'urls': urls,
            'has_listeners': listeners_module is not None,
            'listeners': listeners_module,
            'has_templates': has_templates,
            'template_path': template_path,
            'has_static': has_static,
            'static_path': static_path
        }

