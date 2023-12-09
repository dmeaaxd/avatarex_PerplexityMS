import grpc
import asyncio
from proto import service_pb2_grpc, service_pb2
import os
from dotenv import load_dotenv

load_dotenv()
Perplexity_API_KEY = os.getenv("Perplexity_API_KEY")


async def chat_client():
    try:
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = service_pb2_grpc.ChatServiceStub(channel)

            request = service_pb2.ChatRequest(
                model="mistral-7b-instruct",
                messages=[
                    {"role": "system", "content": "Be precise and concise."},
                    {"role": "user", "content": "How many stars are there in our galaxy?"},
                    {"role": "assistant", "content": "Many!"},
                    {"role": "user", "content": "What is the name of the biggest star? Say only name."}
                ],
                max_tokens=1000,
                temperature=1.0,
                api_token=Perplexity_API_KEY
            )

            response = await stub.Chat(request)

            print("Success:", response.success)
            print("Message:", response.data.message)
            print("Error:", response.data.error)
            print("Execution Time:", response.execution_time)

    except grpc.aio.AioRpcError as e:
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            print("Error: Unable to connect to the server.")
        else:
            print(f"Error: {e}")


if __name__ == '__main__':
    asyncio.run(chat_client())
