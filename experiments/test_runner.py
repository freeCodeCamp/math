import os


class TestRunner:
    def __init__(self):
        self.catch_exceptions = (
            False if os.environ.get("FCC_ENVIRONMENT") == "TESTING" else True
        )

    def run(self, fn):
        if self.catch_exceptions:
            try:
                fn()
            except AssertionError as e:
                print("Error:", e.args[0])
        else:
            fn()
