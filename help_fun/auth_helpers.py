from passlib.context import CryptContext
import random
import string
from datetime import datetime, timedelta
from jose import JWTError, jwt




# ------------------------- USERNAME GENERATOR ------------------------- #
async def generate_username(user_type: str, user_name: set) -> str:
    # 1. First 3 letters of user_name, capitalized
    part1 = user_type[:3].upper()

    # 2. 3 random digits
    part2 = ''.join(random.choices(string.digits, k=3))

    # 3. First 2 letters of first user_type element, capitalized
    user_name_str = next(iter(user_name), "")
    part3 = user_name_str[:2].upper()

    # 4. 4 random alphanumeric characters (letters or digits)
    part4 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    return f"{part1}{part2}{part3}{part4}"



# ------------------------- HASH PASSWORD GENERATOR ------------------------- #
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)




# ------------------------- JWT TOKEN GENERATOR ------------------------- #
SECRET_KEY = "your-secret-access-key"
REFRESH_SECRET_KEY = "your-secret-refresh-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, is_refresh: bool = False):
    try:
        key = REFRESH_SECRET_KEY if is_refresh else SECRET_KEY
        return jwt.decode(token, key, algorithms=[ALGORITHM])
    except JWTError:
        return None
