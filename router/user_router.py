from fastapi import APIRouter,HTTPException
from DB import getConnection
from models import Data
from typing import Optional

router=APIRouter()
################################################################
###API CHECK###
################################################################

@router.get("/great")
def greet():
    return{"message":"Working"}

################################################################
###DATA CREATION###
################################################################


@router.post("/create")

def create(data:Data):
    global current_id
    current_id+=1
    id=current_id
    name=data.name
    mail=data.mail
    address=data.address
    
    conn=getConnection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM USERS WHERE MAIL=%s",(mail,))
    res=cursor.fetchone()


    if res:
        current_id-=1
        raise HTTPException(status_code=400,detail='User already exist')
    cursor.execute("INSERT INTO USERS(NAME,MAIL,ADDRESS) VALUES(%s,%s,%s)",(name,mail,address))
    curr={'mail':mail,'name':name,'address':address}
    conn.commit()
    cursor.close()
    conn.close()
    return {"Message":"Created","details":{'id':id,**curr}}

################################################################
###DATA FETCH###
################################################################


@router.get('/fetch/{id}')
def show(id:int):
    
    conn=getConnection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM USERS WHERE ID=%s",(id,))
    res=cursor.fetchone()
    if not res:
        raise HTTPException(status_code=400,detail='User not found')
    return{'Details':res}

################################################################
###FETCH BY ANY PARAMETERS###
################################################################

@router.get("/fetchall")
def showall(
    id: Optional[int] = None,
    mail: Optional[str] = None,
    name: Optional[str] = None
):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)

    if id is not None:
        cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
        res = cursor.fetchone()

    elif mail is not None:
        cursor.execute("SELECT * FROM users WHERE mail=%s", (mail,))
        res = cursor.fetchone()

    elif name is not None:
        cursor.execute("SELECT * FROM users WHERE name=%s", (name,))
        res = cursor.fetchone()

    

    cursor.close()
    conn.close()

    if not res:
        return {"status": "Users not found"}

    return {"Data": res}


################################################################
###DATA UPDATE###
################################################################


@router.put('/update/{id}')
def update(id:int,address:str):
    
    conn=getConnection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM USERS WHERE ID=%s",(id,))
    user=cursor.fetchone()
    
    #res=cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()

        raise HTTPException(status_code=400,detail='User not found')
    cursor.execute("UPDATE USERS SET ADDRESS=%s WHERE ID=%s",(address,id))
    conn.commit()
    cursor.close()
    conn.close()
    return{"Status":"updated"}

################################################################
###DATA DELETION###
################################################################

@router.delete('/delete/{id}')
def remove(id:int):
    conn=getConnection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM USERS WHERE ID=%s",(id,))
    user=cursor.fetchone()
    
    #res=cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()

        raise HTTPException(status_code=400,detail='User not found')
    cursor.execute('DELETE FROM USERS WHERE ID=%s',(id,))
    conn.commit()
    cursor.close()
    conn.close()
    return{'Status':f'user {id} is removed'}
