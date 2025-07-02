import asyncio, os


# async def get_embedding(text: str) -> list[float]:
#     loop = asyncio.get_event_loop()
#     embedding = await loop.run_in_executor(executor, embedding_model.encode, text)
#     return embedding.tolist()


# def get_sync_embedding(text: str) -> list[float]:
#     return asyncio.run(get_embedding(text))
