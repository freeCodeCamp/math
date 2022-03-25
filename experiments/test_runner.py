class TestRunner:
    def __init__(self, options):
        self.catch_exceptions = options["catch_exceptions"]

    def run(self, fn):
        if self.catch_exceptions:
            try:
                fn()
            except AssertionError as e:
                print("Error:", e.args[0])
        else:
            fn()
