class SafeDict(dict):
    # Return missing keys as string
    def __missing__(self, key) -> str:
        return '{' + key + '}'
