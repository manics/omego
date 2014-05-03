#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2013 University of Dundee & Open Microscopy Environment
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
Primary launching functions for omego. All Commands
which are present in the globals() of this module
will be presented to the user.
"""

import sys

from framework import main, Stop

from upgrade import InstallCommand, UpgradeCommand
from artifacts import DownloadCommand
from db import DbCommand
from version import Version

from docopt import docopt

def entry_point():
    """
    Usage: omego [-v] [-c CFGFILE [-c ...]] [-h] <command> [<args>...]

    Options:
      -v                  Enable verbose output
      -h, --help          Show help message and exit
      -c CFGFILE, --conf  Configuration files, multiple files will be merged
    """
    try:
        items = [
            (InstallCommand.NAME, InstallCommand),
            (UpgradeCommand.NAME, UpgradeCommand),
            (DownloadCommand.NAME, DownloadCommand),
            (DbCommand.NAME, DbCommand),
            (Version.NAME, Version)
        ]
        itemsmap = dict(it for it in items)

        commands = '\n'.join(
            '    %s  %s' % (it[0], it[1].__doc__) for it in items)

        args = docopt(entry_point.__doc__ + '\n' + commands,
                      version='0.0.0', options_first=True)
        print('global arguments:')
        print(args)
        print('command arguments:')
        argv = [args['<command>']] + args['<args>']
        print(argv)

        try:
            it = itemsmap[args['<command>']]
            if hasattr(it, 'USAGE'):
                print(docopt(it.USAGE, argv=argv))
        except KeyError:
            raise Stop(100, 'Invalid command: %s' % args['<command>'])

        return
        main(items)
    except Stop, stop:
        if stop.rc != 0:
            print "ERROR:", stop
        else:
            print stop
        sys.exit(stop.rc)


if __name__ == "__main__":
    entry_point()
