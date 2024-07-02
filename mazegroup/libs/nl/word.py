class Word():
    def __new__(cls, string: str) -> 'Word':
        chars = "abcdefghijklmnopqrstuvwxyz"
        if type(string) == Word: string = string.string
        string = string.lower().strip()
        if not len(string):
            raise Exception(f"Empty word.")
        for char in string:
            if char not in chars:
                raise Exception(f"Invalid character '{char}'.")
        self = super().__new__(cls)
        self.string = string
        return self

    def __repr__(self):
        return self.string