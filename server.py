import os

import grpc
import asyncio
import signal
from typing import List
from pydantic import BaseModel
import requests
from proto import service_pb2_grpc, service_pb2
import sentry_sdk
import logging
import os
from dotenv import load_dotenv

load_dotenv()
sentry_dsn = os.getenv("SENTRY_DSN")

if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

# Инициализация логгера
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("server.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)



class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: int
    temperature: float
    api_token: str

class ChatServiceImplementation(service_pb2_grpc.ChatServiceServicer):
    async def call_perplexity_api(self, request: ChatRequest):
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {request.api_token}"
        }

        payload = {
            "model": request.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages]
        }

        response = await asyncio.to_thread(requests.post, url, json=payload, headers=headers)

        if response.status_code == 200:
            perplexity_result = response.json()
            choices = perplexity_result.get("choices", [])

            if choices:
                assistant_message = next(
                    (choice["message"]["content"] for choice in choices if choice["message"]["role"] == "assistant"),
                    None,
                )
                if assistant_message:
                    return {"text": assistant_message,
                            "execution_time": perplexity_result.get("usage", {}).get("total_tokens", 0) / 10}
                else:
                    raise Exception("No assistant message in perplexity API response")
            else:
                raise Exception("No 'choices' field in perplexity API response")

        raise Exception(f"Error from perplexity API: {response.text}")

    async def Chat(self, request: ChatRequest, context):
        try:
            perplexity_result = await self.call_perplexity_api(request)

            response = service_pb2.ChatResponse()
            response.success = True
            response.data.message = perplexity_result["text"]
            response.execution_time = perplexity_result["execution_time"]

            return response
        except Exception as e:
            response = service_pb2.ChatResponse()
            response.success = False
            response.data.error = str(e)

            logger.error(f"Error in Chat service: {e}")
            return response

async def serve():
    server = grpc.aio.server()
    service_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceImplementation(), server)
    listen_addr = "127.0.0.1:50051"
    server.add_insecure_port(listen_addr)
    logger.info(f"Server listening on {listen_addr}")

    stopping_event = asyncio.Event()

    def stop_server(signum, frame):
        logger.info("Received signal to stop server")
        stopping_event.set()

    signal.signal(signal.SIGTERM, stop_server)
    signal.signal(signal.SIGINT, stop_server)

    await server.start()

    try:
        await stopping_event.wait()
    finally:
        await server.stop(None)

if __name__ == "__main__":
    asyncio.run(serve())
