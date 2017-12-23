from formats import formatter


def irc(comment: dict) -> str:
    return formatter.use('irc', comment)
