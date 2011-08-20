#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyvows import Vows, expect
from tornado_pyvows import TornadoHTTPContext

from aero import AeroApp

@Vows.batch
class SomeVows(TornadoHTTPContext):
    def _get_app(self):
        return AeroApp(apps=[
            'aero.apps.healthcheck'
        ])

    class HealthCheckURL(TornadoHTTPContext):
        def topic(self):
            self._http_client.fetch(self._get_url('/healthcheck'), self._stop)
            response = self._wait()
            return response.body

        def should_be_working(self, topic):
            expect(topic).to_equal('WORKING')
