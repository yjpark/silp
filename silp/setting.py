import silp
import os

class Setting:
    def __init__(self, path, language, rules):
        self.path = path
        self.language = language
        self.rules = rules

    def get_rule(self, macro, params, info_prefix):
        result = None
        for rule in self.rules:
            if rule.macro == macro:
                if not rule.params and not params:
                    result = rule
                elif rule.params and params and len(rule.params) == len(params):
                    result = rule
                else:
                    silp.info(info_prefix +
                              silp.format_error('Mismatched Params for Macro: ') +
                              silp.format_param(rule.__str__()))
        if not result:
            if params:
                silp.info(info_prefix + silp.format_error('Macro Not Found: ')
                          + silp.format_param('%s(%s)' % (macro, ', '.join(map(lambda x: x.name, params)))))
            else:
                silp.info(info_prefix +
                          silp.format_error('Macro Not Found: ') +
                          silp.format_param('%s' % macro))
        return result
