#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join

import tornado.web
import tornado.ioloop
from pyvows import Vows, expect
from tornado_pyvows import TornadoHTTPContext

from aero.app import AeroApp

class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello World')

@Vows.batch
class AeroAppVows(Vows.Context):
    class HealthCheckVows(TornadoHTTPContext):
        def get_app(self):
            return AeroApp(installed_apps=[
                'aero.apps.healthcheck'
            ])

        class HealthCheckURL(TornadoHTTPContext):
            def topic(self):
                self.http_client.fetch(self.get_url('/healthcheck'), self.stop)
                response = self.wait()
                return response.body.strip()

            def should_be_working(self, topic):
                expect(topic).to_equal('WORKING')

    class TemplateOverrideVows(TornadoHTTPContext):
        def get_app(self):
            return AeroApp(installed_apps=[
                'aero.apps.healthcheck'
            ], **{
                'template_path': abspath(join(dirname(__file__), 'templates'))
            })

        class HealthCheckURL(TornadoHTTPContext):
            def topic(self):
                self.http_client.fetch(self.get_url('/healthcheck'), self.stop)
                response = self.wait()
                return response.body.strip()

            def should_be_working(self, topic):
                expect(topic).to_equal('WORKINGTEST')

    class OverrideRoutesVows(TornadoHTTPContext):
        def get_app(self):
            return AeroApp([
                (r'/hello', HelloWorldHandler)
            ],
            installed_apps=[
                'aero.apps.healthcheck'
            ], **{
                'template_path': abspath(join(dirname(__file__), 'templates'))
            })

        class HelloWorldURL(TornadoHTTPContext):
            def topic(self):
                self.http_client.fetch(self.get_url('/hello'), self.stop)
                response = self.wait()
                return response.body.strip()

            def should_be_hello_world(self, topic):
                expect(topic).to_equal('Hello World')


if __name__ == '__main__':
    AeroApp(installed_apps=[
        'aero.apps.healthcheck'
    ], **{
        'template_path': abspath(join(dirname(__file__), 'templates'))
    }).listen(8888)

    tornado.ioloop.IOLoop.instance().start()
