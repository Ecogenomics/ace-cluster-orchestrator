from typing import List, Tuple

from redis import Redis
from rq import Queue

from worker import add_numbers

REDIS_HOST = 'db.gtdb.ecogenomic.org'  # doesn't change
REDIS_PASS = ''                        # from BitWarden
QUEUE_NAME = 'QUEUE_NAME'              # must be unique


def enqueue_jobs(numbers: List[Tuple[int, int]]):
    # It's more efficient to bulk enqueue jobs than to enqueue one at a time.
    to_enqueue = list()
    for number_a, number_b in numbers:
        to_enqueue.append(Queue.prepare_data(
            add_numbers,               # from worker.py
            timeout='1h',              # max runtime of job until stopped and failed
            ttl='20m',                 # max time job can sit in queue before discarding
            failure_ttl='30d',         # max time to store failed job
            result_ttl='1d',           # max time to store successful job
            args=(number_a, number_b)  # arguments to pass to worker
        ))

    # Connect to redis and submit the jobs
    with Redis(host=REDIS_HOST, password=REDIS_PASS) as conn:
        q = Queue(QUEUE_NAME, connection=conn)
        q.enqueue_many(to_enqueue)


def main():
    todo = [(1, 2), (3, 4), (5, 6)]
    enqueue_jobs(todo)


if __name__ == '__main__':
    main()
