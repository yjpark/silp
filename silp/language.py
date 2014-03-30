class Language:
    def __init__(self, name, extension, comment):
        self.name = name
        self.extension = extension
        self.comment = comment

languages = [
    Language('Python', 'py', '#'),
    Language('C#', 'cs', '//'),
    Language('Go', 'go', '//'),
]
