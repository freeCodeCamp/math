from user_env import singleton as user_env
import re


def step01():
    assert (
        user_env.getVariable("var") == "demo"
    ), "var should contain the 'demo' string!"
    assert re.search("'\w*'", user_env.getCode()), "single quotes please!"
    print("Step 01: Success!")


def step02():
    assert (
        user_env.getVariable("a") == "ay"
    ), "variable a should contain the 'ay' string!"
    assert (
        user_env.getVariable("b") == "bee"
    ), "variable b should contain the 'bee' string!"
    print("Step 02: Success!")


def prepare(user_globals, user_input):
    user_env.setGlobals(user_globals)
    user_env.setInput(user_input)
