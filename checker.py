import asyncio
import json
import os

import aioredis
from databases import Database

from clients import setup_nats
from dto import BlobRefDTO
from quering_utils import global_query, shard_query

# config from env vars, with defaults
CHUNK_SIZE = os.getenv("CHUNK_SIZE", 1000)
GLOBAL_DB_URL = os.getenv(
    "GLOBAL_DB_URL", "mysql://global:passglobal@localhost:33333/global"
)
SHARD_DB_URL = os.getenv(
    "SHARD_DB_URL", "mysql://shard:passglobal@localhost:33334/shard"
)
REDIS_HOST = os.getenv("REDIS_HOST", "redis://localhost")
NATS_HOST = os.getenv("NATS_HOST", "nats://localhost:4222")
NATS_SUBJECT = os.getenv("NATS_SUBJECT", "to_check")


async def process_blob(blob, num_ref, nc):
    sent_msg, sent_att = await global_query(blob, global_db)
    body, header, att, out_att, contact_data = await shard_query(blob, shard_db)
    json_msg = BlobRefDTO(
        blob_id=blob,
        num_ref=num_ref,
        sent_msg=sent_msg,
        sent_att=sent_att,
        body=body,
        header=header,
        att=att,
        out_att=out_att,
        contact_data=contact_data,
    )
    await nc.publish(NATS_SUBJECT, json.dumps(json_msg).encode())


async def fetch_blobs(global_db, start_index, last_index):
    query = """SELECT BlobStorageID, NumReferences FROM BlobStorage WHERE NumReferences > 0 AND BlobStorageID BETWEEN :start AND :end """
    blobs = await global_db.fetch_all(
        query, values={"start": start_index, "end": last_index}
    )
    return blobs


async def run(chunk_size, loop, global_db, shard_db):
    # connect to dbs
    await global_db.connect()
    await shard_db.connect()
    redis = await aioredis.create_redis_pool(REDIS_HOST)
    # get last index to allow scaling horizontally and avoid quering same
    start_index = await redis.get("last_id")
    if start_index is None:
        start_index = 0
    last_index = int(start_index) + chunk_size
    await redis.set("last_id", last_index)
    # connect to message queue
    nc = await setup_nats(loop, NATS_HOST)
    blobs = await fetch_blobs(global_db, start_index, last_index)
    # run queries for each blob concurrently
    await asyncio.gather(*[process_blob(blob, num_ref, nc) for blob, num_ref in blobs])
    await global_db.disconnect()
    await shard_db.disconnect()
    await nc.close()
    return last_index, last_index + len(blobs)


if __name__ == "__main__":
    # POSSIBLE TODO - allow setting running periodically
    global_db = Database(GLOBAL_DB_URL)
    shard_db = Database(SHARD_DB_URL)
    eventloop = asyncio.get_event_loop()
    task = eventloop.create_task(
        run(
            chunk_size=CHUNK_SIZE,
            loop=eventloop,
            global_db=global_db,
            shard_db=shard_db,
        )
    )
    eventloop.run_until_complete(task)
