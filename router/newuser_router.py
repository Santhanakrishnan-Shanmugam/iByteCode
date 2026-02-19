from fastapi import APIRouter, HTTPException
from typing import Optional
#from models import Data
from newDB import getDB
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from newDB import getDB  # your dataset DB connection

# ---------------- Pydantic Models ----------------
class Address(BaseModel):
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    zip: str

    class Config:
        extra = "allow"  # allow extra fields dynamically

class Data(BaseModel):
    name: str
    mail: str
    address:Address

    class Config:
        extra = "allow"  # allow extra fields dynamically

# ---------------- Setup DB ----------------
router = APIRouter()
db = getDB()
users = db["users"]
address = db["address"]

# ---------------- CREATE ----------------
@router.post("/create")
def create(user: Data):
    # Check if user already exists
    
    if users.find_one(mail=user.mail):
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Insert user without address
    user_data = user.dict(exclude={"address"})
    user_id = users.insert(user_data)
    
    # Insert address with user_id
    address_data = {"id": user_id, **user.address.dict()}
    address.insert(address_data)

    return {
        "message": "User created",
        "data": {
            **user_data,
            "address": address_data
        }
    }


# ---------------- FETCH ALL / FILTER ----------------

@router.get("/fetchall")
def fetch_all(
    id: Optional[int] = None,
    mail: Optional[str] = None,
    name: Optional[str] = None
):
    if id is not None:
        res = users.find_one(id=id)
        add=address.find_one(id=id)
    elif mail is not None:
        res = users.find_one(mail=mail)
        
        if res:
            add=address.find_one(id=res['id'])
    elif name is not None:
        res = users.find_one(name=name)
        if res:
            add=address.find_one(id=res['id'])
    
    if not res:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": res,"address":add}


# ---------------- FETCH BY ID ----------------

@router.get("/fetch/{id}")
def fetch_by_id(id: int):
    res = users.find_one(id=id)
    if res:
        add=address.find_one(id=res["id"])
    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": res,"address":add}


# ---------------- UPDATE ----------------

@router.put("/update/{id}")
def update(
    id: int,
    line1: Optional[str] = None,
    line2: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip: Optional[str] = None
):
    res = users.find_one(id=id)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {}

    if line1 :
        update_data["line1"] = line1
    if line2 :
        update_data["line2"] = line2
    if city :
        update_data["city"] = city
    if state :
        update_data["state"] = state
    if zip :
        update_data["zip"] = zip

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    id=res['id']
    address.update({'id':id,** update_data} ,["id"])

    return {
        "message": "User updated",
        "updated_fields": update_data
    }


# ---------------- DELETE ----------------

@router.delete("/delete/{id}")
def delete(id: int):
    res = users.find_one(id=id)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")

    users.delete(id=id)
    return {"message": "User deleted"}
