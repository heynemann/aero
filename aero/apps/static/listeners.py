#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from os.path import exists, splitext

import clevercss
from slimmer import css_slimmer

from aero.apps.static.jsmin import jsmin


def get_extension(path):
    return splitext(path)[-1] 

def change_extension(path, from_ext, to_ext):
    return re.sub('%s$' % from_ext, to_ext, path)

def process_static(app):
    def process_js(file_details):
        if app.settings.get('minify_js', False):
            file_details['contents'] = jsmin(file_details['contents'])

    def process_css(file_details):
        if app.settings.get('minify_css', False):
            file_details['contents'] = css_slimmer(file_details['contents'])

    def process_ccss(file_details):
        file_details['contents'] = clevercss.convert(file_details['contents'])

    def process(bus, file_details):
        if get_extension(file_details['path']['path']) == '.ccss':
            process_ccss(file_details)
        if get_extension(file_details['path']['original']) == '.css':
            process_css(file_details)
        if get_extension(file_details['path']['original']) == '.js':
            process_js(file_details)

    return process

def static_not_found(app):
    def find(bus, file_path):
        path = file_path['path']
        if not path: return

        extension = splitext(path)[-1]
        if extension == '.css':
            new_path = change_extension(path, 'css', 'ccss')
            if exists(new_path):
                file_path['path'] = new_path

    return find

def listen(app):
    app.subscribe('static-not-found', static_not_found(app))
    app.subscribe('before-static', process_static(app))
