from user_env import singleton as user_env
import re


def step01():
    assert re.search(
        "def sqrt", user_env.code()
    ), "Please define a function named 'sqrt'."
    actual = user_env.var("sqrt")(25)
    assert actual == 5, "sqrt(25) should return 5, but got " + str(actual)
    print("Step 01: Success!")


def step02():
    assert user_env.var("a") == "ay", "variable a should contain the 'ay' string!"
    assert user_env.var("b") == "bee", "variable b should contain the 'bee' string!"
    print("Step 02: Success!")


def prepare(user_globals, user_input):
    user_env.set_globals(user_globals)
    user_env.set_input(user_input)
