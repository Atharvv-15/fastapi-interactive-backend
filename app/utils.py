from passlib.context import CryptContext

#Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Create a function to hash passwords
def hash(password: str):
    return pwd_context.hash(password)

#Create a function to verify passwords
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

