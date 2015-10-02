import os
import re
import sys
import shutil
import traceback
import imp

import silp
import term
import rule

loaded_plugin_modules = {}

def prepare_dir(path):
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    if not os.path.isdir(dirpath):
        term.error('Can not create dir at: ' + term.format_path(dirpath))
        sys.exit(10)

def get_temp_path(project_path, temp_path, relpath):
    return os.path.join(os.path.expanduser('~'), temp_path, project_path.replace(os.path.sep, '_'), relpath)

def process_file(project, path):
    if '.silp_backup' in path or '.silp_test' in path:
        return
    using_silp = False
    for line in open(path, 'r').readlines():
        if project.language.generated_suffix in line or project.language.macro_prefix in line:
            using_silp = True
            break
    if not using_silp:
        term.verbose('Skipping File That Not Using SILP: ' + path)
        return

    term.info('Processing File: ' + term.format_path(path))
    relpath = os.path.relpath(path, project.path)
    if silp.test_mode:
        input_path = path
        output_path = get_temp_path(project.path, '.silp_test', relpath)
        prepare_dir(output_path)
    else:
        input_path = get_temp_path(project.path, '.silp_backup', relpath)
        prepare_dir(input_path)
        shutil.copy2(path, input_path)
        output_path = path
    process(project, input_path, output_path, relpath)


def process(project, input_path, output_path, relpath):
    term.verbose('Processing: ' +
                 term.format_path(input_path) + ' -> ' +
                 term.format_path(output_path))
    output_lines = []

    line_number = 0
    for line in open(input_path, 'r').readlines():
        line_number = line_number + 1
        if project.language.generated_suffix in line:
            pass
        elif not silp.clean_mode and project.language.macro_prefix in line:
            output_lines.extend(process_macro(project, line, relpath, line_number))
        else:
            output_lines.append(line)
    open(output_path, 'w').writelines(output_lines)

def generate_lines_rule(matched_rule, params):
    generated_lines = []
    for template_line in matched_rule.template:
        new_line = template_line
        if matched_rule.params:
            for i in range(len(matched_rule.params)):
                new_line = new_line.replace('${%s}' % matched_rule.params[i].name, params[i].name)
        generated_lines.append(new_line)
    return generated_lines

def generate_lines_plugin(project, module, func, params):
    try:
        global loaded_plugin_modules
        module_lib = loaded_plugin_modules.get(module)
        if module_lib is None:
            term.verbose('Loading plugin macro: %s %s' % (module, func))
            m = imp.find_module(module, [os.path.join(project.path, 'silp_plugins')])
            module_lib = imp.load_module(module, m[0], m[1], m[2])
            loaded_plugin_modules[module] = module_lib
        term.verbose('Calling plugin macro: %s:%s(%s)' % (module, func, params))
        lines = None
        if params:
            lines = getattr(module_lib, func)(*[p.name for p in params])
        else:
            lines = getattr(module_lib, func)()
        #for line in lines: term.verbose(line)
        return lines
    except Exception as e:
        term.error('Load plugin failed: %s:%s -> %s' % (module, func, e))
        term.error(traceback.format_exc())
        return None

def process_macro(project, line, relpath, line_number):
    result = [line]
    m = re.match(r'(\s*)__SILP__(.*)',
                 line.replace(project.language.macro_prefix, '__SILP__'))
    if m:
        leading_space = m.group(1)
        line = m.group(2).strip()
        generated_lines = None

        if rule.is_plugin_macro(line):
            module, func, params = rule.parse_plugin_macro(line)
            if module and func:
                generated_lines = generate_lines_plugin(project, module, func, params)
        else:
            macro, params = rule.parse_macro(line)
            if macro:
                matched_rule = project.get_rule(macro, params,
                                                '%s:%s ' % (relpath, line_number))
                if matched_rule:
                    generated_lines = generate_lines_rule(matched_rule, params)

        if generated_lines:
            columns = project.language.columns + 1  # the extra 1 is for \n
            for new_line in generated_lines:
                columns = max(len(leading_space) + len(new_line) + 1 +
                              len(project.language.generated_suffix),
                              columns)

            for new_line in generated_lines:
                new_line = '%s%s' % (leading_space, new_line)
                new_line = new_line.replace('\n', '')
                while len(new_line) + len(project.language.generated_suffix) < columns:
                    new_line = new_line + ' '
                new_line = new_line + project.language.generated_suffix
                result.append(new_line)
    return result
