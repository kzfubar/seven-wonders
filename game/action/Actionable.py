class Actionable:
    def __init__(self, func, argv):
        self.func = func
        self.argv = argv

    def run(self):
        self.func(*self.argv)
