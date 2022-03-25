class UserEnv:
    def set_globals(self, user_globals):
        self.globals = user_globals

    def set_input(self, input):
        self.input = input

    def var(self, key):
        return self.globals[key]

    def code(self):
        return self.input[-1]


singleton = UserEnv()
