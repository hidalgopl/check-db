import asyncio
import json

from databases import Database
from nats.aio.client import Client as NATS

global_db = Database("mysql://global:passglobal@localhost:33333/global")
shard_db = Database("mysql://shard:passglobal@localhost:33334/shard")

async def global_query(blob_id):
    query = """SELECT COUNT(BlobStorageID) FROM SentMessage WHERE BlobStorageID = :id"""
    query2 = """SELECT COUNT(BlobStorageID) FROM SentAttachment WHERE BlobStorageID = :id"""
    sent_msg = await global_db.fetch_one(query, values={"id": blob_id})
    sent_att = await global_db.fetch_one(query2, values={"id": blob_id})
    return sent_msg[0], sent_att[0]


async def shard_query(blob_id):
    count_body = """SELECT COUNT(Body) FROM MessageData WHERE Body = :id"""
    count_header = """SELECT COUNT(Header) FROM MessageData WHERE Header = :id"""
    count_att = """SELECT COUNT(BlobStorageID) FROM Attachment WHERE BlobStorageID = :id"""
    count_outside_att = """SELECT COUNT(BlobStorageID) FROM OutsideAttachment WHERE BlobStorageID = :id"""
    count_cont_data = """SELECT COUNT(BlobStorageID) FROM ContactData WHERE BlobStorageID = :id"""
    print(f"checking {blob_id} in shard")
    body = await shard_db.fetch_one(count_body, values={"id": blob_id})
    header = await shard_db.fetch_one(count_header, values={"id": blob_id})
    att = await shard_db.fetch_one(count_att, values={"id": blob_id})
    outside_att = await shard_db.fetch_one(count_outside_att, values={"id": blob_id})
    cont_data = await shard_db.fetch_one(count_cont_data, values={"id": blob_id})
    print(f"got: {body}, {header}, {att}, {outside_att}, {cont_data}")
    return body[0], header[0], att[0], outside_att[0], cont_data[0]


async def run(start_index, last_index, loop):
    await global_db.connect()
    await shard_db.connect()
    print("global & shard connected")
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"], loop=loop)
    print("nats connected")
    query = """SELECT BlobStorageID, NumReferences FROM BlobStorage WHERE NumReferences > 0 AND BlobStorageID BETWEEN :start AND :end """
    blobs = await global_db.fetch_all(query, values={"start": start_index, "end": last_index})
    blobs_objs = {blob_id: num_ref for blob_id, num_ref in blobs}
    for blob, num_ref in blobs_objs.items():
        sent_msg, sent_att = await global_query(blob)
        body, header, att, out_att, contact_data = await shard_query(blob)
        json_msg = {
            "blob_id": blob,
            "num_ref": num_ref,
            "sent_msg": sent_msg,
            "sent_att": sent_att,
            "body": body,
            "header": header,
            "att": att,
            "out_att": out_att,
            "contact_data": contact_data
        }
        await nc.publish("to_check", json.dumps(json_msg).encode())
    await global_db.disconnect()
    await shard_db.disconnect()
    await nc.close()
    return last_index, last_index + len(blobs_objs)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(
        run(start_index=10, last_index=30, loop=loop)
    )
    loop.run_until_complete(task)


#
# def main():
#     start_index = int(os.getenv("LAST_BLOB_ID"))
#     chunk_size = int(os.getenv("CHUNK_SIZE"))
#     last_index = start_index + chunk_size