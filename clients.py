from nats.aio.client import Client as NATS


async def setup_nats(loop, nats_host):
    nc = NATS()
    await nc.connect(servers=[nats_host], loop=loop)
    return nc
