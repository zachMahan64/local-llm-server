from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import ollama, json

app = FastAPI()
MODEL = "gemma4"
sessions: dict[str, list] = {}  # session_id -> message history


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    client = ollama.Client()
    history = sessions.setdefault(req.session_id, [])
    history.append({"role": "user", "content": req.message})

    def generate():
        full_response = ""
        for chunk in client.chat(model=MODEL, messages=history, stream=True):
            content = chunk.message.content
            if content is None:
                continue
            full_response += str(content)
            yield content  # stream tokens as plain text

        history.append({"role": "assistant", "content": full_response})

    return StreamingResponse(generate(), media_type="text/plain")


@app.delete("/chat/{session_id}")
def clear(session_id: str):
    sessions.pop(session_id, None)
    return {"cleared": session_id}
