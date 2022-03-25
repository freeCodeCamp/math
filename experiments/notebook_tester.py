import websocket
import requests
import json
import uuid
from datetime import datetime

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


def create_execute_request(code):
    return create_message(
        "execute_request", {"code": code, "silent": False, "allow_stdin": True}
    )


def create_input_reply(value):
    return create_message("input_reply", {"value": value}, "stdin")


def create_message(msg_type, content, channel="shell"):
    return {
        "header": create_header(msg_type),
        "parent_header": {},
        "metadata": {},
        "content": content,
        "channel": channel,
    }


def create_header(msg_type):
    return {
        "msg_id": str(uuid.uuid4()),
        "username": "test",
        "session": session,
        "date": datetime.now().isoformat(),
        "msg_type": msg_type,
        "version": "5.0",
    }


ws = websocket.WebSocket()
ws.connect("ws://" + jupyter_host + "/api/kernels/" + kernel_info["id"] + "/channels")

# TODO: each entry in 'code' should either be a test or not. If it is a test it
# needs a solution and a seed.  The seed should generate errors then the
# solution should not. If it's not a test, it does not need a solution and
# should execute without errors.
for seed in seed_code:
    req = create_execute_request(seed)
    print("Sending:", req)
    ws.send(json.dumps(req))
    processing = True
    while processing:
        res = json.loads(ws.recv())
        if res["msg_type"] == "execute_reply":
            # TODO: check that the seed fails
            if res["content"]["status"] == "error":
                print("Error:", res)
            else:
                print("Success:", res)
            processing = False
        if res["msg_type"] == "input_request":
            # TODO: use the right input for this request
            req = create_input_reply("dummy data")
            print("Sending reply:", req)
            ws.send(json.dumps(req))

ws.close()
