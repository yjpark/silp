import os
import re
import sys
import shutil
import silp
import rule

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
    silp.verbose('Processing: ' + silp.format_path(input_path) + ' -> ' + silp.format_path(output_path))
    output_lines = []

    line_number = 0
    for line in open(input_path, 'r').readlines():
        line_number = line_number + 1
        if project.language.generated_suffix in line:
            pass
        elif project.language.macro_prefix in line:
            output_lines.extend(process_macro(project, line, relpath, line_number))
        else:
            output_lines.append(line)
    open(output_path, 'w').writelines(output_lines)

def process_macro(project, line, relpath, line_number):
    result = [line]
    m = re.match(r'(\s*)__SILP__(.*)', line.replace(project.language.macro_prefix, '__SILP__'))
    if m:
        leading_space = m.group(1)
        macro, params = rule.parse_macro(m.group(2).strip())
        matched_rule = project.get_rule(macro, params, '%s:%s ' % (relpath, line_number))
        if matched_rule:
            for template_line in matched_rule.template:
                new_line = template_line.replace('\n', '')
                if matched_rule.params:
                    for i in range(len(matched_rule.params)):
                        new_line = new_line.replace('${%s}' % matched_rule.params[i].name, params[i].name)
                new_line = '%s%s' % (leading_space, new_line)
                while len(new_line) + len(project.language.generated_suffix) < project.language.columns:
                    new_line = new_line + ' '
                new_line = new_line + project.language.generated_suffix + '\n'
                result.append(new_line)
    return result
