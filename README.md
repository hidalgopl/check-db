
## Architecture
Solution contains 4 main components
1. [DB getter](checker.py)  - service which calls DBs, puts the results together and publishes them in message queue.
2. Message queue [NATS](https://nats.io) - decouples DB getter and worker, allows to run multiple workers & getters. NATS also ensures that only one worker is processing published message.
3. [Worker](worker.py) - here is where business logic lives. It listens to new messages from queue and process them one at the time. Can be easily scaled horizontally.
4. Key-value store [Redis](https://redis.io/documentation) - this is used to store last checked BlobStorageID.

## Considerations

### Efficiency & speed
This may be not very efficient, as I'm far from being SQL queries expert. This is the biggest issue in this solution.

### Resiliency
It's pretty resilient as getters dump last checked index to Redis.

### Scaling
You can scale both getter & worker horizontally. Only limitation here is DB resistant for such heavy load of queries.

## Running
You'll need docker-compose installed.
1. run `make install_deps` to install required python libraries.
2. `make setup_env` will turn on docker-compose services (NATS, both databases & redis).
3. `make a_mess` will introduce inconsistencies in DB.
4. `make look_for_incosistent` will run single worker which will wait for new messages in queue & process them. It prints inconsistent entries to stdout, can be easily dumped to a file.
5. `make fetch_from_db` is a service which runs DB queries and publishes BlobRefDTO objects to message queue.


## Testing
You can run unit tests for business logic via `make tests`.
