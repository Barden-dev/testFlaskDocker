import time
import redis
import redis.exceptions
import os

from flask import Flask
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
redis_host = os.getenv('redis_host', 'redis')

print(redis_host)

cache = redis.Redis(host=redis_host, port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1 
            time.sleep(0.5)



@app.route('/')
def hello():
    count = get_hit_count()
    return f"<h1>Привет от Docker!</h1><p>Это приложение работает в контейнере.</p> <p>Эту страницу просмотрели {count} раз.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
