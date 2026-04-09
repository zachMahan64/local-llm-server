import ollama

MODEL = "gemma4"


def do_repl():
    print("Hi, I'm bot.")
    client = ollama.Client()
    messages = []

    while True:
        inp = input(">> ")
        if inp in ("q", "quit"):
            break

        messages.append({"role": "user", "content": inp})

        full_response = ""
        for chunk in client.chat(model=MODEL, messages=messages, stream=True):
            content = chunk.message.content
            print(content, end="", flush=True)
            full_response += str(content)

        print("")
        messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    do_repl()
