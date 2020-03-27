import asyncio
import json
import os

from business_logic import Handler
from clients import setup_nats
from dto import BlobRefDTO

NATS_HOST = os.getenv("NATS_HOST", "nats://localhost:4222")


async def run(loop):
    nc = await setup_nats(loop, NATS_HOST)
    sid = await nc.subscribe("to_check", "workers", subscribe_handler)


async def subscribe_handler(msg):
    data = BlobRefDTO(**json.loads(msg.data.decode()))
    handler = Handler(dto=data)
    handler.process()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(run(loop=loop))
    loop.run_forever()
