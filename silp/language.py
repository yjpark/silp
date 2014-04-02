import silp

class Language:
    def __init__(self, name, extension, macro_prefix, generated_suffix, columns):
        self.name = name
        self.extension = extension
        self.macro_prefix = macro_prefix
        self.generated_suffix = generated_suffix
        self.columns = columns

languages = [
    Language('Python', '.py', '#SILP:', '#__SILP__\n', 80),
    Language('C#', '.cs', '//SILP:', '//__SILP__\n', 80),
    Language('Go', '.go', '//SILP:', '//__SILP__\n', 80),
]
