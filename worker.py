import asyncio
import json

from nats.aio.client import Client as NATS


async def run(loop):
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"], loop=loop)
    sid = await nc.subscribe("to_check", "workers", subscribe_handler)


def check_data_consistency(data):
    real_num_ref = data["sent_msg"] + data["sent_att"] + data["body"] + data["header"] + data["att"] + data["out_att"] + data["contact_data"]
    if data["num_ref"] != real_num_ref:
        print(f"DATA INCONSISTENT:\n#{data['blob_id']} Num ref: {data['num_ref']} != {real_num_ref}\n{data}")


async def subscribe_handler(msg):
    data = json.loads(msg.data.decode())
    check_data_consistency(data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(
        run(loop=loop)
    )
    loop.run_forever()
