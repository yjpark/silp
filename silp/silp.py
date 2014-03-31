import os
import sys
import argparse
import glob
import plistlib
import datetime
import pytz
from blessings import Terminal

import language
from setting import Setting
from rule import Rule
import processor

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

def format_error(err):
    return term.red(err)

def format_path(path):
    return term.blue(path)

def format_param(param):
    return term.yellow(param)

def read_macro(line):
    line = line.replace('\n', '').strip()
    if len(line) < 3 or line[0] != '#' or line[-1] != '#':
        error('Invalid Macro Definition, Must Look Like: "# MACRO_NAME #": ' + format_param(line))
        sys.exit(6)
    else:
        macro = line[1:-2]
        return macro.strip()

def is_template_tag(line):
    return line.startswith('```')

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
        else:
            template.append(line)
    if not macro is None or not template is None:
        error('Incomplete Rule: %s\n%s' % (macro, template))
        sys.exit(5)
    if verbose_mode:
        verbose('Rules:')
        for rule in rules:
            verbose('    %s' % rule);
    return rules

def load_project(path=None):
    if path:
        path = os.path.abspath(path)
    else:
        path = os.path.abspath(os.getcwd())
    verbose('Loading Project Info: ' + format_path(path))
    #get the project setting file's path
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
    #find proper language setting
    extension = os.path.basename(project_path).replace('silp_', '.').replace('.md', '')
    project_language = None
    for lang in language.languages:
        if lang.extension == extension:
            project_language = lang
            break
    if not project_language:
        error('Unsupported Language: ' + format_param(extension))
        sys.exit(4)
    else:
        verbose('Project Language: ' + format_param(project_language.name))
    return Setting(path, project_language, load_rules(project_path))

def process_all(project):
    files = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(project.path)
            for f in files if f.endswith(project.language.extension)]
    for path in files:
        processor.process_file(project, path)

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
        project = load_project()
        process_all(project)
    elif args.file:
        project = load_project(os.path.dirname(args.file[0]))
        for path in args.file:
            processor.process_file(project, path)
    else:
        info('Please provide the files to process, or use "--all" to process all files')
        sys.exit(1)
