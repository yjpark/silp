import silp

class Language:
    def __init__(self, name, extension, macro_tag, generated_tag):
        self.name = name
        self.extension = extension
        self.macro_tag = macro_tag
        self.generated_tag = generated_tag

languages = [
    Language('Python', '.py', '#SILP:', '#__SILP__'),
    Language('C#', '.cs', '//SILP:', '//__SILP__'),
    Language('Go', '.go', '//SILP:', '//__SILP__'),
]
