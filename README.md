
## Architecture
Solution contains 3 main components
1. DB getter  - service which periodically calls DBs, puts the results together and publishes them in message queue.
2. Message queue - component which stores DB entries to be checked if any inconsistencies occurs.
3. Checker - here is where business logic lives. It listens to new messages from queue and process them one at the time. Can be easily scaled horizontally.


## Considerations

### Efficiency
This may be not very efficient, as I'm not SQL queries expert. In real life I'd consult my queries with someone who has more knowledge in this topic.

### Speed
Should be good.

### Resiliency

### Scaling
Since DB objects are dumped to message queue, it's really easy to scale the workers.

