#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import tornado.web

class HealthcheckHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('aero/healthcheck/working.html')
