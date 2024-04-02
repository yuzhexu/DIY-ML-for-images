from rq import Worker, Queue, Connection
from redis import Redis

# connect to redis
redis_conn = Redis(host='localhost', port=6379, db=0)
queue_names = ['training', 'inference']  # identify queues name

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, queue_names))
        worker.work()
