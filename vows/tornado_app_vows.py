#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
import tornado.ioloop
from pyvows import Vows, expect
from tornado_pyvows import TornadoHTTPContext

from aero import AeroApp

@Vows.batch
class AeroAppVows(Vows.Context):
    class HealthCheckVows(TornadoHTTPContext):
        def get_app(self):
            return AeroApp(apps=[
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
            return AeroApp(apps=[
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


if __name__ == '__main__':
    AeroApp(apps=[
        'aero.apps.healthcheck'
    ], **{
        'template_path': abspath(join(dirname(__file__), 'templates'))
    }).listen(8888)

    tornado.ioloop.IOLoop.instance().start()
