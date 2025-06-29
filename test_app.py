from app import app
from dotenv import load_dotenv
import os

def test_hello():
    load_dotenv()
    redis_host = os.getenv('redis_host', 'redis')
    
    print(redis_host)
    
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200