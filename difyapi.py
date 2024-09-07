import asyncio
import requests
import json
from typing import List, Dict, AsyncGenerator, Optional
from sseclient import SSEClient
from concurrent.futures import ThreadPoolExecutor

class AsyncDifyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.dify.ai/v1/chat-messages"
        self.session = requests.Session()
        self.executor = ThreadPoolExecutor(max_workers=5)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.executor.shutdown(wait=False)

    async def chat_completion_stream(
        self, 
        messages: List[Dict[str, str]], 
        user: str,
        conversation_id: Optional[str] = None
    ) -> AsyncGenerator[Dict, None]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Extract the last user message as the query
        query = next((msg['content'] for msg in reversed(messages) if msg['role'] == 'user'), "")

        data = {
            "inputs": {},
            "query": query,
            "response_mode": "streaming",
            "conversation_id": conversation_id or "",
            "user": user
        }

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            self.executor,
            lambda: self.session.post(self.base_url, headers=headers, json=data, stream=True)
        )

        client = SSEClient(response)
        for event in client.events():
            if event.event == "message":
                data = json.loads(event.data)
                yield {
                    "choices": [
                        {
                            "delta": {
                                "content": data['answer']
                            },
                            "finish_reason": None
                        }
                    ],
                    "id": data['message_id'],
                    "conversation_id": data['conversation_id'],
                    "created": data['created_at']
                }
            elif event.event == "message_end":
                data = json.loads(event.data)
                yield {
                    "choices": [
                        {
                            "delta": {},
                            "finish_reason": "stop"
                        }
                    ],
                    "id": data['id'],
                    "conversation_id": data['conversation_id'],
                    "usage": data['metadata']['usage']
                }
                break