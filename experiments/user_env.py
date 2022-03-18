class UserEnv:
    def setGlobals(self, user_globals):
        self.globals = user_globals

    def setInput(self, input):
        self.input = input

    def getVariable(self, key):
        return self.globals[key]

    def getCode(self):
        return self.input[-1]


singleton = UserEnv()
