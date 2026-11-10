
class mirror:
    def __init__(self, name, url, cursor=None):
        self.name = name
        self.url = url
        self.db_cursor = cursor
    def syncdb(self):
        return self

class distro():
    def __init__(self):
        return self

class component():
    def __init__(self, arch):
        self.arch = arch
class architecture():
    def __init__(self, arch):
        self.arch = arch