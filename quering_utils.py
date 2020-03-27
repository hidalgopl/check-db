async def global_query(blob_id, global_db):
    query = """SELECT COUNT(BlobStorageID) FROM SentMessage WHERE BlobStorageID = :id"""
    query2 = (
        """SELECT COUNT(BlobStorageID) FROM SentAttachment WHERE BlobStorageID = :id"""
    )
    sent_msg = await global_db.fetch_one(query, values={"id": blob_id})
    sent_att = await global_db.fetch_one(query2, values={"id": blob_id})
    return sent_msg[0], sent_att[0]


async def shard_query(blob_id, shard_db):
    count_body = """SELECT COUNT(Body) FROM MessageData WHERE Body = :id"""
    count_header = """SELECT COUNT(Header) FROM MessageData WHERE Header = :id"""
    count_att = (
        """SELECT COUNT(BlobStorageID) FROM Attachment WHERE BlobStorageID = :id"""
    )
    count_outside_att = """SELECT COUNT(BlobStorageID) FROM OutsideAttachment WHERE BlobStorageID = :id"""
    count_cont_data = (
        """SELECT COUNT(BlobStorageID) FROM ContactData WHERE BlobStorageID = :id"""
    )
    print(f"checking {blob_id} in shard")
    body = await shard_db.fetch_one(count_body, values={"id": blob_id})
    header = await shard_db.fetch_one(count_header, values={"id": blob_id})
    att = await shard_db.fetch_one(count_att, values={"id": blob_id})
    outside_att = await shard_db.fetch_one(count_outside_att, values={"id": blob_id})
    cont_data = await shard_db.fetch_one(count_cont_data, values={"id": blob_id})
    print(f"got: {body}, {header}, {att}, {outside_att}, {cont_data}")
    return body[0], header[0], att[0], outside_att[0], cont_data[0]
