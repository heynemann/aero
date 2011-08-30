#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys
from os.path import abspath, dirname, join, exists, split, splitext
from os import curdir
import os
import optparse
import imp
import fnmatch

import tornado.ioloop
from tornado.httpserver import HTTPServer

from aero.app import AeroApp

DEFAULT_IP = "0.0.0.0"
DEFAULT_PORT = 3333
server = None

def main(args=sys.argv):
    '''Runs aero server with the specified arguments.'''

    if len(args) < 2:
        print "aero should be called with the command you want to run. i.e.: aero serve or aero collectstatic"
        return

    command = args[1]
    args.remove(command)

    if not command in COMMANDS:
        print 'The command %s is not supported by aero. Available commands are: %s' % (command, ', '.join(COMMANDS.keys()))
        print 'If you want help on a specific command, type aero <<command>> -h, like aero serve -h'
        return

    command = COMMANDS[command]

    parser = optparse.OptionParser(usage="aero or type aero -h (--help) for help", description=__doc__, version="0.1.0")

    command = command(parser)
    command.configure()

    (opt, args) = parser.parse_args()

    command.options = opt
    command.args = args

    command.run()

class BaseCommand(object):
    def load_conf(self, conf_path):
        conf = conf_path and abspath(conf_path) or None
        if not conf or not exists(conf):
            conf = abspath(join(dirname(curdir), 'aero.conf'))
            if not exists(conf):
                return None

        conf_file = split(conf)[-1]
        conf_path = dirname(conf)
        conf_module = imp.load_source(conf_file, conf, open(conf))
        os.remove(join(dirname(conf), "%sc" % conf_file))

        return conf_module

class AeroServerCommand(BaseCommand):
    def __init__(self, parser):
        self.parser = parser

    def configure(self):
        self.parser.add_option("-p", "--port", type="int", dest="port", default=DEFAULT_PORT, help = "The port to run at [default: %default]." )
        self.parser.add_option("-i", "--host", dest="host", default=DEFAULT_IP, help = "The ip address to run at [default: %default]." )
        self.parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help = "Indicates that the app should be run in debug mode [default: %default]." )
        self.parser.add_option("-c", "--conf", dest="conf", default=None, help = "The path for the aero.conf file. If not specified, defaults to the app folder [default: %default]." )

    def run(self):
        conf_module = self.load_conf(self.options.conf)
        if not conf_module:
            print "The configuration file must be specified and be present."
            return

        settings = {}
        for key in dir(conf_module):
            if not key.startswith('_') and hasattr(conf_module, key):
                settings[key] = getattr(conf_module, key)
        settings["debug"] = self.options.debug

        app = AeroApp(**settings)

        self.run_app(self.options.host, self.options.port, app, self.options.debug)

    def run_app(self, ip, port, app, debug):
        self.server = HTTPServer(app)
        self.server.bind(port, ip)
        self.server.start(1)

        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            print
            print "-- aero closed by user interruption --"


class CollectStaticCommand(BaseCommand):
    def __init__(self, parser):
        self.parser = parser

    def configure(self):
        self.parser.add_option("-c", "--conf", dest="conf", default=None, help = "The path for the aero.conf file. If not specified, defaults to the app folder [default: %default]." )
        self.parser.add_option("-o", "--output", dest="output", default=None, help = "The path for the collected statics. If not specified, defaults to a 'static' folder in the app folder [default: %default]." )
        self.parser.add_option("-i", "--ignore", dest="ignore", action='append', default=['.DS_Store', '*.swp', '*.swo'], help = "File patterns to ignore [default: %default]." )

    def run(self):
        conf_module = self.load_conf(self.options.conf)
        settings = {}
        for key in dir(conf_module):
            if not key.startswith('_') and hasattr(conf_module, key):
                settings[key] = getattr(conf_module, key)

        application = AeroApp(**settings)

        if not exists(self.options.output):
            os.makedirs(self.options.output)

        print 'Copying static files to %s' % self.options.output
        print 'Ignoring %s' % ', '.join(self.options.ignore)
        print

        root = None
        if hasattr(conf_module, 'static_path'):
            root = conf_module.static_path
            for root, dirs, files in os.walk(root):
                for static in files:
                    ignore = False
                    for pattern in self.options.ignore:
                        if fnmatch.fnmatch(static, pattern):
                            ignore = True
                            break
                    if ignore: continue
                    static = join(root, static).replace(root, '').lstrip('/')
                    self.write_static_to(self.options.output, static, application, root=root)

        for app in application.apps:
            static_files_path = join(app['path'], 'static')
            for root, dirs, files in os.walk(static_files_path):
                for static in files:
                    ignore = False
                    for pattern in self.options.ignore:
                        if fnmatch.fnmatch(static, pattern):
                            ignore = True
                            break
                    if ignore: continue

                    static = join(root, static).replace(static_files_path, '').lstrip('/')
                    self.write_static_to(self.options.output, static, application, root=root, apps=application.apps)

        print
        print 'Static files copied.'

    def write_static_to(self, output, static, application, root=None, apps=[], search=True):
        static = static.lstrip('/')
        target_path = abspath(join(output.rstrip('/'), static))

        def write(file_data):
            print "Writing '%s' to '%s'" % (file_data['path'], file_data['target_path'])
            if not exists(dirname(file_data['target_path'])):
                os.makedirs(dirname(file_data['target_path']))
            with open(file_data['target_path'], 'w') as target:
                target.write(file_data['contents'])

        if root:
            path = abspath(join(root, static))
            if exists(path):
                contents = open(path).read()
                resulting_file = {
                    'path': path,
                    'filename': split(path)[-1],
                    'extension': splitext(path)[-1].lstrip('.'),
                    'contents': contents,
                    'target_path': target_path
                }
                application.publish('before-static', resulting_file)
                write(resulting_file)
                application.publish('post-static', resulting_file)
                return

        if apps:
            for app in apps:
                path = abspath(join(app['path'], 'static', static))
                if exists(path):
                    contents = open(path).read()
                    resulting_file = {
                        'path': path,
                        'filename': split(path)[-1],
                        'extension': splitext(path)[-1].lstrip('.'),
                        'contents': contents,
                        'target_path': target_path
                    }
                    application.publish('before-static', resulting_file)
                    write(resulting_file)
                    application.publish('after-static', resulting_file)
                    return

COMMANDS = {
    'serve': AeroServerCommand,
    'collectstatic': CollectStaticCommand
}

if __name__ == "__main__":
    main()


