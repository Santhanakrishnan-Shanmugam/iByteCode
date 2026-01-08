from fastapi import FastAPI
from dotenv import load_dotenv
import os
import uvicorn

from router.create_router import router as create_router
from router.read_router import router as read_router
from router.update_router import router as update_router
from router.delete_router import router as delete_router
from router.user_router import router as user_router
from router.readall_router import router as readall_router
from router.newuser_router import router as updated_router
from mongo_user import router as mongorouter
load_dotenv()  # LOAD .env file

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

app = FastAPI()

app.include_router(user_router, prefix="/api/users")
#app.include_router(mongorouter,prefix="/api/users")
@app.get("/")
def g():
    return {"message": "From run"}

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host=HOST,
        port=PORT,
        reload=True
    )
