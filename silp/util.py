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
from . import term

test_mode = False
clean_mode = False


def read_macro(line):
    line = line.replace('\n', '').strip()

    if len(line) < 3 or line[0] != '#' or line[-1] != '#':
        return None
    else:
        macro = line[1:-1]
        return macro.strip()


def is_template_tag(line):
    return line.startswith('```')


def read_include_path(line):
    line = line.replace('\n', '').strip()
    if len(line) < 5 or line[0] != '<' or line[1] != '<' and line[2] != '[' or line[-1] != ']':
        return None
    else:
        path = line[3:-1]
        return path.strip()


def include_in_template(template, project_path, include_path):
    include_path = os.path.join(os.path.dirname(project_path), include_path)
    if os.path.isfile(include_path):
        lines = open(include_path).readlines()
        for line in lines:
            template.append(line)
    else:
        term.error('Include File Not Found: ' + term.format_path(include_path))


def load_rules(project_path):
    lines = open(project_path).readlines()
    rules = []
    macro = None
    template = None
    for line in lines:
        if macro is None:
            if line.strip():
                macro = read_macro(line)
        elif is_template_tag(line):
            if template is None:
                template = []
            else:
                rules.append(Rule(macro, template))
                macro = None
                template = None
        elif template is not None:
            include_path = read_include_path(line)
            if include_path:
                include_in_template(template, project_path, include_path)
            else:
                template.append(line)

    if not macro is None or not template is None:
        term.error('Incomplete Rule: %s\n%s' % (macro, template))
        sys.exit(5)
    term.verbose('Rules:')
    for rule in rules:
        term.verbose('    %s' % rule)
    return rules


def get_project_pathes(path):
    if path:
        path = os.path.abspath(path)
    else:
        path = os.path.abspath(os.getcwd())
    # get the project setting file's path
    while os.path.exists(path):
        matches = glob.glob(os.path.join(path, 'silp_*.md'))
        if len(matches) == 0:
            path = os.path.dirname(path)
        else:
            return matches
    return None

