import os
import sys
import argparse
import glob
import plistlib
import datetime
import pytz

import language
from setting import Setting
from rule import Rule
import processor
import term

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


def load_projects(path=None):
    if path:
        path = os.path.abspath(path)
    else:
        path = os.path.abspath(os.getcwd())
    term.verbose('Loading Project Info: ' + term.format_path(path))
    project_pathes = get_project_pathes(path)
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
                                  load_rules(project_path)))
    return result


def process_all(project):
    files = [os.path.join(dirpath, f)
             for dirpath, dirnames, files in os.walk(project.path)
             for f in files if f.endswith(project.language.extension)]
    for path in files:
        project_pathes = get_project_pathes(path)
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

    global test_mode
    test_mode = args.test
    global clean_mode
    clean_mode = args.clean

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
