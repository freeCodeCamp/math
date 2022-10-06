from user_env import singleton as user_env


def step01():
    print('User\'s "var" variable is set to "demo"?')
    print(user_env.getVariable("var") == "demo")
    print("User's code")
    print(user_env.getCode())


def prepare(user_globals, user_input):
    user_env.setGlobals(user_globals)
    user_env.setInput(user_input)
