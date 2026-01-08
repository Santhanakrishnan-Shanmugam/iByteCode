from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from typing import Optional
class Data(BaseModel):
    name:str
    mail:str
    address:str

class Del(BaseModel):
    mail:str
class Update(BaseModel):
    mail:str
    address:str

user={}
current_id=0
app=FastAPI()

@app.get("/")
def greet():
    return {'message':"Hello world"}


@app.post('/create')
def create(data:Data):
    global current_id
    current_id+=1
    id=current_id
    name=data.name
    mail=data.mail
    address=data.address

    for i in user:
        if mail in user[i]['mail']:
            current_id-=1
            raise HTTPException(status_code=400,detail='User already exist')
    user[id]={'mail':mail,'name':name,'address':address}
    return {"Message":"Created","details":{'id':id,**user[id]}}

@app.put('/api/update/{id}')
def update(id:int,address:str):
    if id not in user:
        raise HTTPException(status_code=400,detail='User not found')
    temp=user[id]['address']
    user[id]['address']=address
    return{"Status":temp + ' is updated to ' + address}

@app.get('/api/fetch/{id}')
def show(id:int):
    
    if id not in user:
        raise HTTPException(status_code=400,detail='User not found')
    return{'Details':user[id]}


@app.get('/api/fetchall')
def showall(gid:Optional[int]=None,
            mail:Optional[str]=None,
            name:Optional[str]=None):
    
    result=[]
    for userid,detail in user.items():
        if gid is not None and gid!=userid:
            continue
        if mail is not None and mail != detail['mail']:
            continue
        if name is not None and name != detail['name']:
            continue
        result.append({"id": userid, **detail})
    if not result:
        return{'status':'Users not found'}
    return{
        "Data":result
    }

@app.delete('/delete')
def remove(data:Del):
    
    if data.mail not in user:
        raise HTTPException(status_code=400,detail='user not found')
    user.pop(data.mail)
    return{'Status':'user '+data.mail+' is removed'}
        