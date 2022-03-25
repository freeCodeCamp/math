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


def wait_for_execution(seed):
    processing = True
    # TODO: this is ugly, is there a way to know that the "execute_reply" came
    # from a seed or a solution? metadata?
    testing_seed = True
    while processing:
        res = json.loads(ws.recv())
        if res["msg_type"] == "execute_reply":
            # TODO: refactor this ugly code
            has_error = res["content"]["status"] == "error"
            if testing_seed and has_error:
                req = create_execute_request(soln)
                print("seed failed")
                testing_seed = False
                ws.send(json.dumps(req))
            elif testing_seed and not has_error:
                print("seed passed", seed)
                raise Exception("tests should fail on seeds")
            elif has_error:
                print("solution failed", soln)
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
req = create_execute_request(seed_code[0])
try:
    ws.send(json.dumps(req))
    wait_for_execution(seed_code[0])
except Exception as e:
    print("Error on seed is expected, currently:", e.args[0])

for (seed, soln) in zip(seed_code[1:], solutions):
    req = create_execute_request(seed)
    print("Sending:", req)
    ws.send(json.dumps(req))
    wait_for_execution(seed)


ws.close()
