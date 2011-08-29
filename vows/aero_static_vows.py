#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import abspath, join, dirname

from pyvows import Vows, expect
from tornado_pyvows import TornadoHTTPContext

from aero.app import AeroApp

STATIC_PATH = abspath(join(dirname(__file__), 'static'))

@Vows.batch
class AeroStaticFileVows(Vows.Context):

    class WithRootPath(TornadoHTTPContext):
        def get_app(self):
            return AeroApp(static_path=STATIC_PATH)

        class CheckStaticURL(TornadoHTTPContext):
            def topic(self):
                self.http_client.fetch(self.get_url('/static/file.txt'), self.stop)
                response = self.wait()
                return response.body.strip()

            def should_be_working(self, topic):
                expect(topic).to_equal('aero')

    class AppWithoutRootPath(TornadoHTTPContext):
        def get_app(self):
            return AeroApp(installed_apps=[
                    'fixtures.apps.staticapp'
                ])

        class CheckStaticURL(TornadoHTTPContext):
            def topic(self):
                self.http_client.fetch(self.get_url('/static/file.txt'), self.stop)
                response = self.wait()
                return response.body.strip()

            def should_be_working(self, topic):
                expect(topic).to_equal('staticapp')

    class WithAppAndRootPath(TornadoHTTPContext):
        def get_app(self):
            return AeroApp(installed_apps=[
                    'fixtures.apps.staticapp'
                ], static_path=STATIC_PATH)

        class CheckStaticURL(TornadoHTTPContext):
            def topic(self):
                self.http_client.fetch(self.get_url('/static/file.txt'), self.stop)
                response = self.wait()
                return response.body.strip()

            def should_be_working(self, topic):
                expect(topic).to_equal('aero')

