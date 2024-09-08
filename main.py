
import asyncio
from difyapi import AsyncDifyClient

import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


DIFY_API_KEY = os.getenv("DIFY_API_KEY")

TASK_CONVERSATION_MAP = {}

async def chat_stream(client,messages, task_id, conversation_id):
    async for chunk in client.chat_completion_stream(messages, user=task_id, conversation_id=conversation_id):
        if task_id:
            conversation_id = TASK_CONVERSATION_MAP.get(task_id)
            if not conversation_id:
                conversation_id = chunk['conversation_id']
                TASK_CONVERSATION_MAP[task_id] = conversation_id

        data = json.dumps({
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": 1677858242,
            "model": "gpt-4o",
            "choices": chunk['choices']
        })
        yield "data: " + data + "\n\n"


@app.post("/chat/completions")
async def chat(request: Request):
    data = await request.json()
    messages = data.get("messages", [])

    client = AsyncDifyClient(DIFY_API_KEY)
    
    # for trtc ai conversation
    task_id = request.headers.get("X-Task-Id")
    request_id = request.headers.get("X-Request-Id")

    conversation_id = None
    if task_id:
        conversation_id = TASK_CONVERSATION_MAP.get(task_id)

    return StreamingResponse(chat_stream(client,messages, task_id, conversation_id), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)