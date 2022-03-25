import websocket
import requests
import json
import uuid
from datetime import datetime
from solutions import solutions

notebook_filename = "notebook.ipynb"
jupyter_host = "localhost:8888"
kernel_url = "http://" + jupyter_host + "/api/kernels"

kernel_info = json.loads(requests.post(kernel_url).text)
session = str(uuid.uuid4())

notebook_url = "http://" + jupyter_host + "/api/contents/" + notebook_filename
notebook = json.loads(requests.get(notebook_url).text)

# TODO: separate out the cells with tests from those without
seed_code = list(
    map(
        lambda cell: cell["source"],
        filter(lambda cell: cell["cell_type"] == "code", notebook["content"]["cells"]),
    )
)

# username is used to differentiate between the seed, solution and setup code
def create_execute_request(code, username):
    return create_message(
        "execute_request",
        {"code": code, "silent": False, "allow_stdin": True},
        "shell",
        username,
    )


def create_input_reply(value):
    return create_message("input_reply", {"value": value}, "stdin")


def create_message(msg_type, content, channel, username="seed"):
    return {
        "header": create_header(msg_type, username),
        "parent_header": {},
        "metadata": {},
        "content": content,
        "channel": channel,
    }


def create_header(msg_type, username):
    return {
        "msg_id": str(uuid.uuid4()),
        "username": username,
        "date": datetime.now().isoformat(),
        "msg_type": msg_type,
        "version": "5.0",
    }


ws = websocket.WebSocket()
ws.connect("ws://" + jupyter_host + "/api/kernels/" + kernel_info["id"] + "/channels")


def wait_for_execution(seed):
    processing = True
    while processing:
        res = json.loads(ws.recv())
        if res["msg_type"] == "execute_reply":
            # TODO: refactor this ugly code
            has_error = res["content"]["status"] == "error"
            username = res["parent_header"].get("username")
            if username == "seed" and has_error:
                req = create_execute_request(soln, "solution")
                print("seed failed")
                ws.send(json.dumps(req))
            elif username == "seed" and not has_error:
                print("seed passed", seed)
                raise Exception("tests should fail on seeds")
            elif has_error:
                print(username, "failed", soln)
                print(res)
                raise Exception("tests should not fail on solutions")
            else:
                processing = False

        if res["msg_type"] == "input_request":
            # TODO: use the right input for this request
            req = create_input_reply("dummy data")
            print("Sending reply:", req)
            ws.send(json.dumps(req))


# TODO: find a better way to differentiate between setup and test cells.
# Assuming that the first cell is the only setup cell is brittle.
req = create_execute_request(seed_code[0], "setup")
ws.send(json.dumps(req))
wait_for_execution(seed_code[0])


for (seed, soln) in zip(seed_code[1:], solutions):
    req = create_execute_request(seed, "seed")
    print("Sending:", req)
    ws.send(json.dumps(req))
    wait_for_execution(seed)


ws.close()
