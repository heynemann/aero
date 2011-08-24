#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect
from tornado_pyvows import TornadoHTTPContext

from aero.app import AeroApp

@Vows.batch
class BusVows(Vows.Context):

    class CanPublishFromAppVows(TornadoHTTPContext):
        def get_app(self):
            return AeroApp()

        class CanPublishVows(TornadoHTTPContext):
            def topic(self):
                was_called = { 'called': False }
                def callback(bus, was_called):
                    was_called['called'] = True

                self.app.subscribe('some.event', callback)

                self.app.publish('some.event', was_called)

                return was_called

            def should_be_working(self, topic):
                expect(topic).not_to_be_an_error()
                expect(topic).to_be_true()


