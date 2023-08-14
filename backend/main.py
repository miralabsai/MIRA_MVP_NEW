from fastapi import FastAPI
from src.api import user_route  # Import the user_route module
from logger import get_logger
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.utils import auth


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this based on your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

app.include_router(user_route.router, prefix="/api", tags=["users"])
log = get_logger(__name__)

@app.get("/")
def read_root():
    log.info("Hello Mira")
    return {"Hello": "MIRA"}

 # at last, the bottom of the file/module
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)