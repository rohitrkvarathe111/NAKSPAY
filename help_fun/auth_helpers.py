from passlib.context import CryptContext
import random
import string




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
