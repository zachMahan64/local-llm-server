import requests, uuid

SESSION = str(uuid.uuid4())  # gets unique conversation id
DEFAULT_ADDR = "http://10.37.33.12:8000"


def do_repl():
    server = DEFAULT_ADDR
    print("Hi, I'm a robot.")

    want_ip_inp = input("Have a specific IP in mind? [y/n]")

    if want_ip_inp.lower() == "y":
        ip = input("Enter IP: ")
        server = f"http://{ip}:8000"

    while True:
        inp = input(">> ")
        if inp in ("q", "quit"):
            requests.delete(f"{server}/chat/{SESSION}")
            break
        with requests.post(
            f"{server}/chat", json={"session_id": SESSION, "message": inp}, stream=True
        ) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
                print(chunk, end="", flush=True)
        print("")


if __name__ == "__main__":
    do_repl()
