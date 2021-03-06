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
import webbrowser

from launchpadlib import launchpad
import pkg_resources


__version__ = pkg_resources.require('next-bug')[0].version

LAUNCHPAD_CACHE_DIR = os.path.expanduser('~/.launchpadlib/cache/')


def render_bugs(bugs, maximum=None):
    class Colorize(object):
        NORMAL = '\033[0m'
        LINK = '\x1b[34m'

        @property
        def enabled(cls):
            return os.environ.get('CLICOLOR')

        def link(cls, s):
            return cls.LINK + s + cls.NORMAL if cls.enabled else s

    colorize = Colorize()

    for bug in bugs[:maximum]:
        print colorize.link(bug.web_link), bug.title.strip()


def find_new_bugs(project):
    return project.searchTasks(status='New')


def find_unprioritized_bugs(project):
    bugs = project.searchTasks(importance='Undecided')

    # incomplete bugs can't necessarily be prioritized
    return [x for x in bugs if x.status != 'Incomplete']


def sort_bugs_by_date_created(bugs):
    return sorted(bugs, key=lambda bug: bug.date_created)


def get_launchpad_client():
    class NoCredentialProvided(Exception):
        pass

    def no_credentials():
        raise NoCredentialProvided()

    try:
        return launchpad.Launchpad.login_with(
            'next-bug', 'production', LAUNCHPAD_CACHE_DIR,
            credential_save_failed=no_credentials)
    except NoCredentialProvided:
        return launchpad.Launchpad.login_anonymously(
            'next-bug', 'production', LAUNCHPAD_CACHE_DIR)


def main(args):
    lp = get_launchpad_client()

    for project_name in args.projects:
        project = lp.projects[project_name]
        for query in [
                find_new_bugs,
                find_unprioritized_bugs]:
            bugs = sort_bugs_by_date_created(query(project))
            if bugs:
                render_bugs(bugs, maximum=1)
                webbrowser.open(bugs[0].web_link)
                sys.exit(len(bugs))


def cli():
    parser = argparse.ArgumentParser(
        prog='next-bug',
        description='Manage Launchpad bugs without any hassle.')
    parser.add_argument(
        'projects', metavar='project', nargs='+',
        help='Projects to include when prioritizing bugs.')
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
