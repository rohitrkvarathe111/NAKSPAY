from passlib.context import CryptContext
import random
import string
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer






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



# ------------------------- ACCOUNT NAME GENERATOR ------------------------- #

async def generate_account_num(account_type: str, acc_id: int, name: str) -> str:
    name = name.split()[0]
    type_code = account_type[:2].upper()
    id_part = f"{acc_id:02}"

    ran_latter = ''.join(random.choices(string.ascii_uppercase, k=3))

    if len(name) < 4:
        pad_length = 4 - len(name)
        random_letters = ''.join(random.choices(string.ascii_uppercase, k=pad_length))
        name_part = name.upper() + random_letters
    else:
        name_part = name.upper()

    return f"{type_code}{id_part}{ran_latter}-{name_part}"



# ------------------------- HASH PASSWORD GENERATOR ------------------------- #
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_password(email: str, length: int = 10) -> str:
    if len(email) < 3:
        raise ValueError("Email must be at least 3 characters long")
    
    prefix = email[:3]
    remaining_length = length - len(prefix)
    
    characters = string.ascii_letters + string.digits
    random_part = ''.join(random.choices(characters, k=remaining_length))
    
    return prefix + random_part




# ------------------------- JWT TOKEN GENERATOR ------------------------- #
SECRET_KEY = "NaksPay_Secret_key"
REFRESH_SECRET_KEY = "NaksPay_Secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 150
REFRESH_TOKEN_EXPIRE_DAYS = 7


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

blacklisted_tokens = set()

def blacklist_token(token: str):
    blacklisted_tokens.add(token)

def is_token_blacklisted(token: str) -> bool:
    return token in blacklisted_tokens


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

    if is_token_blacklisted(token):
        return None
    try:
        key = REFRESH_SECRET_KEY if is_refresh else SECRET_KEY
        return jwt.decode(token, key, algorithms=[ALGORITHM])
    except JWTError:
        return None
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    # auth_user = payload.get("sub")
    # if auth_user is None:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    return payload

