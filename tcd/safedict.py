class SafeDict(dict):
    """
    SafeDict retains keys that do not exist
    """

    def __missing__(self, key) -> str:
        """
        Return missing key as string
        :param key:
        :return:
        """
        return '{' + key + '}'
