#!/usr/bin/python
# -*- coding: utf-8 -*-


def process_static(app):
    def process_js(file_details):
        pass
    def process_css(file_details):
        pass
    def process_ccss(file_details):
        pass
    def process(bus, file_details):
        import ipdb;ipdb.set_trace()

    return process

def listen(app):
    import ipdb;ipdb.set_trace()
    app.subscribe('before-static', process_static(app))
