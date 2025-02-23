

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from routes import  userRoute
from routes import  ingRoute, authRoute 
from typing import List
from typing_extensions import Annotated



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

origins = {
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:4040",
    "https://127.0.0.1:37953",
    "http://127.0.0.1:3000",
    "http://localhost:3000/?",
    "http://localhost:19006",
    
        
}

app.add_middleware(
   CORSMiddleware,
    allow_origins = ["*"],
    #allow_origins = origins,
    allow_credentials =True,
    allow_methods = ["*"],
    allow_headers= ["*"],
)


app.include_router(userRoute.router)
app.include_router(ingRoute.router)
app.include_router(authRoute.router) 


