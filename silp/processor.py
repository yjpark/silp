import os
import re
import sys
import shutil
import silp
import rule
import imp

loaded_plugin_modules = {}

def prepare_dir(path):
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    if not os.path.isdir(dirpath):
        silp.error('Can not create dir at: ' + silp.format_path(dirpath))
        sys.exit(10)


def process_file(project, path):
    if '.silp_backup' in path or '.silp_test' in path:
        return
    using_silp = False
    for line in open(path, 'r').readlines():
        if project.language.generated_suffix in line or project.language.macro_prefix in line:
            using_silp = True
            break
    if not using_silp:
        silp.verbose('Skipping File That Not Using SILP: ' + path)
        return

    silp.info('Processing File: ' + silp.format_path(path))
    relpath = path.replace(project.path + os.path.sep, '')
    if silp.test_mode:
        input_path = path
        output_path = os.path.join(project.path, '.silp_test', relpath)
        prepare_dir(output_path)
    else:
        input_path = os.path.join(project.path, '.silp_backup', relpath)
        prepare_dir(input_path)
        shutil.copy2(path, input_path)
        output_path = path
    process(project, input_path, output_path, relpath)


def process(project, input_path, output_path, relpath):
    silp.verbose('Processing: ' +
                 silp.format_path(input_path) + ' -> ' +
                 silp.format_path(output_path))
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

def load_from_file(filepath):
    class_inst = None
    expected_class = 'MyClass'

    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, expected_class):
        class_inst = getattr(py_mod, expected_class)()

    return class_inst

def generate_lines_plugin(module, func, params):
    try:
        global loaded_plugin_modules
        module_lib = loaded_plugin_modules.get(module)
        if module_lib is None:
            silp.verbose('Loading plugin macro: %s %s' % (module, func))
            module_find = imp.find_module(module, [os.path.join(project.path, 'silp_plugins')])
            module_lib = imp.load_module(module, m[0], m[1], m[2])
            loaded_plugin_modules[module] = module_lib
        silp.verbose('Calling plugin macro: %s:%s(%s)' % (module, func, params))
        if params:
            return module_lib.getattr(func)(*params)
        else:
            return module_lib.getattr(func)()
    except Exception as e:
        silp.error('Load plugin failed: %s:%s -> %s' % (module, func, e))
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
                enerated_lines = generate_lines_plugin(module, func, params)
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
                columns = max(len(leading_space) + len(new_line) +
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
