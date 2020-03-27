import asyncio
import os

from databases import Database

SHARD_DB_URL = os.getenv(
    "SHARD_DB_URL", "mysql://shard:passglobal@localhost:33334/shard"
)


async def run(shard_db):
    await shard_db.connect()
    query = """UPDATE MessageData SET Body = 2211 WHERE MessageID = 9781975; UPDATE Attachment SET BlobStorageID = 14 WHERE AttachmentID IN (121373, 121374, 121376, 121377)"""
    await shard_db.execute(query)


if __name__ == "__main__":
    shard_db = Database(SHARD_DB_URL)
    eventloop = asyncio.get_event_loop()
    task = eventloop.create_task(run(shard_db=shard_db))
    eventloop.run_until_complete(task)
