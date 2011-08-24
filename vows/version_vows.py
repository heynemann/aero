#!/usr/bin/python
# -*- coding: utf-8 -*-

from types import TupleType
from pyvows import Vows, expect

@Vows.batch
class AeroVersionVows(Vows.Context):

    def topic(self):
        from aero.version import __version__
        return __version__

    def should_be_a_tuple(self, topic):
        expect(topic).to_be_instance_of(TupleType)
