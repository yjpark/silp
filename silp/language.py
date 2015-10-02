import silp
import term


class Language:
    def __init__(self, name, extension, macro_prefix,
                 generated_suffix, columns):
        self.name = name
        self.extension = extension
        self.macro_prefix = macro_prefix
        self.generated_suffix = generated_suffix
        self.columns = columns

languages = [
    Language('Python', '.py', '#SILP:', '#__SILP__\n', 80),
    Language('C#', '.cs', '//SILP:', '//__SILP__\n', 80),
    Language('Go', '.go', '//SILP:', '//__SILP__\n', 80),
    Language('Freshrc', '.freshrc', '#SILP:', '#__SILP__\n', 80),
    Language('YML', '.yml', '#SILP:', '#__SILP__\n', 80),
    Language('Swift', '.swift', '//SILP:', '//__SILP__\n', 80),
    Language('Objective-C', '.m', '//SILP:', '//__SILP__\n', 80),
    Language('Objective-C++', '.mm', '//SILP:', '//__SILP__\n', 80),
    Language('Moonscript', '.moon', '--SILP:', '--__SILP__\n', 80),
    Language('Lua', '.lua', '--SILP:', '--__SILP__\n', 80),
    Language('Erlang', '.erl', '%SILP:', '%__SILP__\n', 80),
    Language('Erlang Include', '.hrl', '%SILP:', '%__SILP__\n', 80),
    Language('SQL', '.sql', '-- SILP:', '/*__SILP__*/\n', 80),
]
