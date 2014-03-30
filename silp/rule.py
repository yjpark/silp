import silp

class PositionParam:
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return '${%s}' % self.index

    def sample_str(self):
        return 'param%s' % self.index


class NamedParam:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '${%s}' % self.name

    def sample_str(self):
        return '%s=xxx' % self.name


class Rule:
    def __init__(self, macro, template):
        self.macro = macro
        self.template = template
        self.params = parse_rule_params(template)

    def __str__(self):
        if self.params:
            return '%s(%s) [%s]' % (self.macro, ', '.join(map(lambda x: x.sample_str(), self.params)), len(self.template))
        else:
            return '%s [%s]' % (self.macro, len(self.template))


def parse_rule_params(template):
    return []
