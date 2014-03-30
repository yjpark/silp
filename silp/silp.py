import os
import sys
import argparse
import glob
import plistlib
import datetime
import pytz
from blessings import Terminal

import setting
import language
import rule

term = Terminal()

test_mode = False
verbose_mode = False

def info(msg):
    print term.normal + msg

def verbose(msg):
    if verbose_mode:
        info(msg)

def error(msg):
    print term.red + msg

def format_path(path):
    return term.blue(path)

def load_project(path=None):
    if path:
        path = os.path.abspath(path)
    else:
        path = os.getcwd()
    verbose('Loading Project Info: ' + format_path(path))
    project_path = None
    while os.path.exists(path):
        matches = glob.glob(os.path.join(path, 'silp_*.md'))
        if len(matches) == 1:
            project_path = matches[0]
            break
        elif len(matches) == 0:
            path = os.path.dirname(path)
        else:
            error('Multiple Silp Setting Found: %s' % matches)
            sys.exit(2)
    if not project_path:
        error('Silp Setting Not Found: ' + format_path(path))
        sys.exit(3)
    else:
        verbose('Silp Setting Found: ' + format_path(project_path))
    extension = project_path.replace('silp_', '').replace('.md', '')
    project_language = None
    for lang in language.languages:
        pass

def process_all():
    verbose('Processing All Files')

def process_one(path):
    info('Processing File: ' + format_path(path))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--test', action='store_true', help='Test Only, Not Overriding Original Files')
    parser.add_argument('-a', '--all', action='store_true', help='Processing All Files in The Current Project')
    parser.add_argument('file', nargs='*')

    args = parser.parse_args()
    global test_mode
    test_mode = args.test
    global verbose_mode
    verbose_mode = args.verbose

    if args.all:
        load_project()
        process_all()
    elif args.file:
        load_project(os.path.dirname(args.file[0]))
        for path in args.file:
            process_one(path)
    else:
        info('Please provide the files to process, or use "--all" to process all files')
        sys.exit(1)
