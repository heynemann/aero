#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys
from os.path import abspath, dirname, join, exists, split
from os import curdir
import optparse
import imp

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
        print 'The command %s is not supported by aero. For a list of commands use aero -h or --help'
        return

    command = COMMANDS[command]

    parser = optparse.OptionParser(usage="aero or type aero -h (--help) for help", description=__doc__, version="0.1.0")

    command = command(parser)
    command.configure()

    (opt, args) = parser.parse_args()

    command.options = opt
    command.args = args

    command.run()

class AeroServerCommand(object):
    def __init__(self, parser):
        self.parser = parser

    def configure(self):
        self.parser.add_option("-p", "--port", type="int", dest="port", default=DEFAULT_PORT, help = "The port to run at [default: %default]." )
        self.parser.add_option("-i", "--host", dest="host", default=DEFAULT_IP, help = "The ip address to run at [default: %default]." )
        self.parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help = "Indicates that the app should be run in debug mode [default: %default]." )
        self.parser.add_option("-c", "--conf", dest="conf", default=None, help = "The path for the aero.conf file. If not specified, defaults to the app folder [default: %default]." )

    def run(self):
        conf = abspath(self.options.conf)
        if not conf or not exists(conf):
            conf = abspath(join(dirname(curdir), 'aero.conf'))
            if not exists(conf):
                print "The configuration file must be specified and be present."
                return

        conf_file = split(conf)[-1]
        conf_path = dirname(conf)
        conf_module = imp.load_source(conf_file, conf_path, open(conf))

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


class CollectStaticCommand(object):
    def __init__(self, parser):
        self.parser = parser

    def configure(self):
        self.parser.add_option("-c", "--conf", dest="conf", default=None, help = "The path for the aero.conf file. If not specified, defaults to the app folder [default: %default]." )


COMMANDS = {
    'serve': AeroServerCommand
}

if __name__ == "__main__":
    main()


