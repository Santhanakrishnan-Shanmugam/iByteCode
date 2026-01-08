from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db1 import get_db
from typing import Optional
from bson import ObjectId
'''
line 1
line 2
city
city
zip

'''
class User(BaseModel):
    class Config:
        extra="allow"

router = APIRouter()
db = get_db()
users = db["users"]

@router.post("/check")
def check(data:User):
    return{"Message":data}
#----------------- CREATE ---------------------------
@router.post("/create")
def create_user(user: User):
    if users.find_one({"mail": user.dict().get("mail")}):
        raise HTTPException(status_code=400, detail="User already exists")

    users.insert_one(user.dict())
    return {"message": "User created", "data": user.dict()}


# ---------------- FETCH ALL ----------------

@router.get("/fetchall")
def fetch_all(
    
    mail: Optional[str] = None,
    name: Optional[str] = None
):
    query={}
    if mail:
        query['mail']=mail
    if name:
        query['name']=name    
    
    res=users.find_one(query)

    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    res["_id"] = str(res["_id"])

    return {"data": res}


# ---------------- FETCH BY ID ----------------

@router.get("/fetch/{id}")
def fetch_by_id(id: str):
    
    res = users.find_one({"_id" : ObjectId(id)})
    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    res["_id"] = str(res["_id"])
    return {"data": res}


# ---------------- UPDATE ----------------

@router.put("/update/{id}")
def update_user(id: str, address: str):
    result = users.update_one(
        {"_id": ObjectId(id)},
        {"$set":{"address": address}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated"}

# ---------------- DELETE ----------------

@router.delete("/delete/{id}")
def delete(id: str):
    res = users.delete_one({"_id":ObjectId(id)})
    if res.deleted_count==0:
        raise HTTPException(status_code=404, detail="User not found")

    
    return {"message": "User deleted"}
