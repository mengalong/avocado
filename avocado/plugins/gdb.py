# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: Red Hat Inc. 2014
# Author: Cleber Rosa <cleber@redhat.com>

"""Run tests with GDB goodies enabled."""

from avocado import runtime
from avocado.utils import process
from avocado.plugins import plugin


class GDB(plugin.Plugin):

    """
    Run tests with GDB goodies enabled
    """

    name = 'gdb'
    enabled = True

    def configure(self, parser):
        self.parser = parser
        gdb_grp = self.parser.runner.add_argument_group('GNU Debugger support')
        gdb_grp.add_argument('--gdb-run-bin', action='append',
                             default=[], metavar='BINARY_PATH',
                             help=('Set a breakpoint on a given binary to be '
                                   'run inside the GNU debugger. Format should '
                                   'be "<binary>[:breakpoint]". Breakpoint '
                                   'defaults to "main"'))

        gdb_grp.add_argument('--gdb-enable-core', action='store_true',
                             default=False,
                             help=('Automatically generate a core dump when the'
                                   ' inferior process received a fatal signal '
                                   'such as SIGSEGV or SIGABRT'))

        default_gdb_path = '/usr/bin/gdb'
        try:
            system_gdb_path = process.find_command('gdb')
        except process.CmdNotFoundError:
            system_gdb_path = default_gdb_path
        gdb_grp.add_argument('--gdb-path',
                             default=system_gdb_path, metavar='PATH',
                             help=('Path to the GDB executable, should you '
                                   'need to use a custom GDB version. Defaults '
                                   'to "%(default)s"'))

        self.configured = True

    def activate(self, app_args):
        try:
            for binary in app_args.gdb_run_bin:
                runtime.GDB_RUN_BINARY_NAMES_EXPR.append(binary)
            if app_args.gdb_enable_core:
                runtime.GDB_ENABLE_CORE = True
            runtime.GDB_PATH = app_args.gdb_path
        except AttributeError:
            pass
