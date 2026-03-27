from fastapi import FastAPI,Depends,HTTPException,Form,UploadFile,File
from sqlmodel import SQLModel,create_engine,Session,select
from contextlib import asynccontextmanager
from typing import Annotated
from models import User,Create_user,User
import os,shutil


DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL,echo=True)
@asynccontextmanager
async def lifespan(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
app = FastAPI(lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session,Depends(get_session)]


UPLOAS_DIRS = "uploads"

os.makedirs(UPLOAS_DIRS,exist_ok=True)

@app.post("/createUser")
def usercreate(
    session:SessionDep,
    name:str=Form(...),
    email:str=Form(...),
    phone:str=Form(...),
    file:UploadFile = File(...)
    
    ):
    user_data = {"name":name,"phone":phone,"email":email}
    validated = Create_user.model_validate(user_data)
    file_path = os.path.join(UPLOAS_DIRS,file.filename)
    with open(file_path,'wb') as f:
        shutil.copyfileobj(file.file,f)
    user = User(**validated.model_dump(),file_path = file.filename)  
    session.add(user)
    session.commit()
    session.refresh(user)
    return user