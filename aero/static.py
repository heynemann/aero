#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from os.path import join, abspath, exists, isdir, isfile, sep, split, splitext
import os
import datetime
import mimetypes
from stat import ST_MTIME
import email.utils
import time

from tornado.web import StaticFileHandler, HTTPError


class AeroStaticFileHandler(StaticFileHandler):

    CACHE_MAX_AGE = 86400*365*10 #10 years

    def initialize(self, path=None, default_filename=None, apps=[]):
        self.root = None
        if path:
            self.root = abspath(path) + sep
        self.default_filename = default_filename
        self.apps = apps

    def get(self, path, include_body=True):
        if sep != "/":
            path = path.replace("/", sep)

        path = path.lstrip('/')
        file_path = None
        if self.root:
            file_path = abspath(join(self.root.rstrip('/'), path))

        if not file_path or not exists(file_path):
            # look in each app's static dir
            for app in self.apps:
                if not app['has_static']:
                    continue
                file_path = abspath(join(app['static_path'].rstrip('/'), path))
                if exists(file_path):
                    break

        if file_path and isdir(file_path) and self.default_filename is not None:
            # need to look at the request.path here for when path is empty
            # but there is some prefix to the path that was already
            # trimmed by the routing
            if not self.request.path.endswith("/"):
                self.redirect(self.request.path + "/")
                return
            file_path = join(file_path, self.default_filename)


        if not file_path or not exists(file_path):
            raise HTTPError(404)
        if not file_path or not isfile(file_path):
            raise HTTPError(403, "%s is not a file", path)

        stat_result = os.stat(file_path)
        modified = datetime.datetime.fromtimestamp(stat_result[ST_MTIME])

        self.set_header("Last-Modified", modified)

        mime_type, encoding = mimetypes.guess_type(file_path)
        if mime_type:
            self.set_header("Content-Type", mime_type)

        cache_time = self.get_cache_time(path, modified, mime_type)

        if cache_time > 0:
            self.set_header("Expires", datetime.datetime.utcnow() + \
                                       datetime.timedelta(seconds=cache_time))
            self.set_header("Cache-Control", "max-age=" + str(cache_time))
        else:
            self.set_header("Cache-Control", "public")

        self.set_extra_headers(path)

        # Check the If-Modified-Since, and don't send the result if the
        # content has not been modified
        ims_value = self.request.headers.get("If-Modified-Since")
        if ims_value is not None:
            date_tuple = email.utils.parsedate(ims_value)
            if_since = datetime.datetime.fromtimestamp(time.mktime(date_tuple))
            if if_since >= modified:
                self.set_status(304)
                return

        if not include_body:
            return

        static_file = open(file_path, 'rb')
        try:
            contents = static_file.read()
        finally:
            static_file.close()

        resulting_file = {
            'last-modified': modified,
            'mime-type': mime_type,
            'encoding': encoding,
            'path': path,
            'filename': split(path)[-1],
            'extension': splitext(path)[-1].lstrip('.'),
            'contents': contents
        }
        self.write(resulting_file['contents'])

    def get_cache_time(self, path, modified, mime_type):
        """Override to customize cache control behavior.

        Return a positive number of seconds to trigger aggressive caching or 0
        to mark resource as cacheable, only.

        By default returns cache expiry of 10 years for resources requested
        with "v" argument.
        """
        return self.CACHE_MAX_AGE if "v" in self.request.arguments else 0
