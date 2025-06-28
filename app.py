import time
from flask import Flask
import redis
import redis.exceptions

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

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
