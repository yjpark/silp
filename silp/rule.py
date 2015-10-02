import re

import silp
import term


class MacroParam:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'MacroParam: %s' % (self.name)


class Rule:
    def __init__(self, line, template):
        self.macro, self.params = parse_macro(line)
        self.template = template

    def __str__(self):
        if self.params:
            return '%s(%s) [%s]' % (self.macro,
                                    ', '.join(map(lambda x: x.name,
                                                  self.params)),
                                    len(self.template))
        else:
            return '%s [%s]' % (self.macro, len(self.template))

def is_plugin_macro(line):
    return line.find(':') > 0

def parse_macro(line):
    macro = None
    params = None
    if '(' in line:
        m = re.match(r'(\w*)\((.*)\)', line)
        if m:
            macro = m.group(1)
            params = [MacroParam(name.strip()) for name in m.group(2).split(',')]
    else:
        m = re.match(r'(\w*)', line)
        if m:
            macro = m.group(1)
            params = None
    return macro, params

def parse_plugin_macro(line):
    module = None
    func = None
    params = None
    if '(' in line:
        m = re.match(r'(\w*):(\w*)\((.*)\)', line)
        if m:
            module = m.group(1)
            func = m.group(2)
            params = [MacroParam(name.strip()) for name in m.group(3).split(',')]
    else:
        m = re.match(r'(\w*):(\w*)', line)
        if m:
            module = m.group(1)
            func = m.group(2)
            params = None
    return module, func, params
