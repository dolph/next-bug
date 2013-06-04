# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import os
import sys

import pkg_resources


__version__ = pkg_resources.require('next-bug')[0].version


def which(program):
    """Locates a program file in the user's path."""
    for path in os.environ['PATH'].split(":"):
        if os.path.exists(path + '/' + program):
            return path + '/' + program


def open_url(url):
    """Opens a URL using whatever program is available on the system."""
    open_app = which('xdg-open') or 'open'
    os.system('%s %s' % (open_app, url))


def main(args):
    sys.exit()


def cli():
    parser = argparse.ArgumentParser(
        prog='next-bug',
        description='Manage Launchpad bugs without any hassle.')
    parser.add_argument(
        '--version', action='store_true',
        help='Show version number and exit')
    args = parser.parse_args()

    if args.version:
        print pkg_resources.require('next-bug')[0]
        sys.exit()

    main(args)


if __name__ == '__main__':
    cli()
