from fastapi import APIRouter,HTTPException
from models import Data
from DB import getConnection
from pydantic import BaseModel
from newDB import getDB


router=APIRouter()
user={}
current_id=0

class Data(BaseModel):
    class Config:
        extra='allow'



@router.post("/create")
def create(data:Data):
    db = getDB()
    users = db["users"]
    
    if users.find_one(mail=data.mail):
        raise HTTPException(status_code=400, detail="User already exists")

    users.insert(data.dict())
    return {"message": "User created", "data": data.dict()}



# @router.post("/create")

# def create(data:Data):
#     global current_id
#     current_id+=1
#     id=current_id
    
    
#     conn=getConnection()
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM USERS WHERE MAIL=%s",(data.mail,))
#     res=cursor.fetchone()


#     if res:
#         current_id-=1
#         raise HTTPException(status_code=400,detail='User already exist')
#     cursor.execute("INSERT INTO USERS(NAME,MAIL,ADDRESS) VALUES(%s,%s,%s)",(data.name,data.mail,data.address))
#     curr={'mail':data.mail,'name':data.name,'address':data.address}
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"Message":"Created","details":{'id':id,**curr}}
