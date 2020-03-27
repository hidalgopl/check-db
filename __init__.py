import os

import databases

global_db = databases.Database(os.getenv("DATABASE_URL"))
shard_db = databases.Database(os.getenv("SHARD_DB_URL"))
