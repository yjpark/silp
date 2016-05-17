from __future__ import absolute_import

import os
import sys
import argparse
import glob
import plistlib
import datetime
import pytz

from . import language
from .setting import Setting
from .rule import Rule
from . import processor
from . import term
from . import util


def load_projects(path=None):
    if path:
        path = os.path.abspath(path)
    else:
        path = os.path.abspath(os.getcwd())
    term.verbose('Loading Project Info: ' + term.format_path(path))
    project_pathes = util.get_project_pathes(path)
    if not project_pathes:
        term.error('Silp Setting Not Found: ' + term.format_path(path))
        sys.exit(3)

    # find proper language setting
    result = []
    for project_path in project_pathes:
        term.verbose('Silp Setting Found: ' + term.format_path(project_path))
        extension = os.path.basename(
            project_path).replace('silp_', '.').replace('.md', '')
        project_language = None
        for lang in language.languages:
            if lang.extension == extension:
                project_language = lang
                break
        if not project_language:
            term.error('Unsupported Language: ' + term.format_param(extension))
        else:
            term.verbose('Project Language: ' + term.format_param(project_language.name))
            result.append(Setting(os.path.dirname(project_path),
                                  project_language,
                                  util.load_rules(project_path)))
    return result


def process_all(project):
    files = [os.path.join(dirpath, f)
             for dirpath, dirnames, files in os.walk(project.path)
             for f in files if f.endswith(project.language.extension)]
    for path in files:
        project_pathes = util.get_project_pathes(path)
        if project_pathes and project.path == os.path.dirname(project_pathes[0]):
            processor.process_file(project, path)
        else:
            term.verbose("Skiping: " + term.format_path(path))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Test Only, Not Overriding Original Files')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Processing All Files in The Current Project')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Clean, Remove Lines Created By SILP')
    parser.add_argument('file', nargs='*')

    args = parser.parse_args()
    term.set_verbose_mode(args.verbose)

    util.test_mode = args.test
    util.clean_mode = args.clean

    if args.all:
        projects = load_projects()
        for project in projects:
            process_all(project)
    elif args.file:
        projects = load_projects(os.path.dirname(args.file[0]))
        for path in args.file:
            for project in projects:
                processor.process_file(project, path)
    else:
        term.info('Please provide the files to process, or use "--all" to process all files')
        sys.exit(1)
