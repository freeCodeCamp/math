# Since the tests are intended to be run locally or in CI we disable the authentication.
c.NotebookApp.disable_check_xsrf = True
c.NotebookApp.token = ""
