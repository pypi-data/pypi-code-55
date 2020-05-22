from pydantic import BaseModel


## Based on tutorial example at 
## https://fastapi.tiangolo.com/tutorial/extra-models/

class BaseUser(BaseModel):
    username: str
    email: str
    full_name: str = None
    role: str

class UserIn(BaseUser):
    password: str

class UserOut(BaseUser):
    pass

class UserInDB(BaseUser):
    hashed_password: str
