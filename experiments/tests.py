from user_env import singleton as user_env
import re

def step01():
    assert user_env.getVariable("var") == "demo", "var should contain the 'demo' string!"
    assert re.search("'\w*'", user_env.getCode()), 'single quotes please!'
    print("Step 01: Success!")


def prepare(user_globals, user_input):
    user_env.setGlobals(user_globals)
    user_env.setInput(user_input)
