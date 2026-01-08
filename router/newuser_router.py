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
    address: Address

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
    elif mail is not None:
        res = users.find_one(mail=mail)
    elif name is not None:
        res = users.find_one(name=name)
    else:
        res = list(users.all())

    if not res:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": res}


# ---------------- FETCH BY ID ----------------

@router.get("/fetch/{id}")
def fetch_by_id(id: int):
    res = users.find_one(id=id)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": res}


# ---------------- UPDATE ----------------

@router.put("/update/{id}")
def update(id: int, address):
    res = users.find_one(id=id)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")

    users.update({"id": id}, address)
    return {"message": "User updated", "updated_fields": address}


# ---------------- DELETE ----------------

@router.delete("/delete/{id}")
def delete(id: int):
    res = users.find_one(id=id)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")

    users.delete(id=id)
    return {"message": "User deleted"}
