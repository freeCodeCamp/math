from user_env import singleton as user_env
import re

def step01():
    print('User\'s "var" variable is set to "demo"?')
    assert user_env.getVariable("var") == "demo", "var should contain the 'demo' string!"
    print("User's code")
    assert re.search("'\w*'", user_env.getCode()), 'single quotes please!'


def prepare(user_globals, user_input):
    user_env.setGlobals(user_globals)
    user_env.setInput(user_input)
