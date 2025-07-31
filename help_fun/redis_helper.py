import redis
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    def __init__(self):
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.db = int(os.getenv('REDIS_DB', 0))
        self.password = os.getenv('REDIS_PASSWORD', None)
        self.decode_responses = True
        self.ssl = os.getenv('REDIS_SSL', False)
        self.client = None

    def connect(self) -> bool:
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=self.decode_responses,
                ssl=self.ssl
            )
            self.client.ping()
            logging.info("Connected to Redis.")
            return True
        except redis.AuthenticationError:
            logging.error("Redis authentication failed.")
            return False
        except redis.ConnectionError as e:
            logging.error(f"Redis connection error: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected Redis error: {e}")
            return False
    
    def hset(self, name: str, key: str, value: str) -> bool:
        if not self.client:
            if not self.connect():
                return False
        try:
            self.client.hset(name, key, value)
            return True
        except Exception as e:
            logging.error(f"Redis HSET error: {e}")
            return False

    def hget(self, name: str, key: str) -> str | None:
        if not self.client:
            if not self.connect():
                return None
        try:
            return self.client.hget(name, key)
        except Exception as e:
            logging.error(f"Redis HGET error: {e}")
            return None
        
    def set_otp(self, email_id: str, otp: str, expire_seconds: int = 30) -> bool:
        if not self.client:
            if not self.connect():
                return False
        try:
            key = f"Users_OTP:{email_id}"
            self.client.set(name=key, value=otp, ex=expire_seconds)
            return True
        except Exception as e:
            logging.error(f"Failed to set OTP in Redis: {e}")
            return False
        
    def get_otp(self, email_id: str) -> str | None:
        if not self.client:
            if not self.connect():
                return None
        try:
            key = f"Users_OTP:otp:{email_id}"
            return self.client.get(key)
        except Exception as e:
            logging.error(f"Failed to get OTP from Redis: {e}")
            return None
    




# redis_client = RedisClient()

# if redis_client.connect():
#     for i in range(10):
#         email_id = f"rohitvarathe{i}@gmail.com"
#         otp = f"7894{i}"
#         if redis_client.set_otp(email_id, otp):
#             print(f"OTP set for user {email_id}")

#         stored_otp = redis_client.get_otp(email_id)
#         print(f"OTP from Redis: {stored_otp}")
# else:
#     print("Redis not connected")


