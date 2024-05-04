from rq import Worker, Queue, Connection
from redis import Redis
import os

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')  # 使用 REDIS_URL 环境变量
redis_conn = Redis.from_url(redis_url)

# connect to redis
queue_names = ['training', 'inference']  # identify queues name

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, queue_names))
        worker.work()
