from fastapi import APIRouter,HTTPException
from router.create_router import user
from DB import getConnection
router=APIRouter()

@router.get('/fetch/{id}')
def show(id:int):
    
    conn=getConnection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM USERS WHERE ID=%s",(id,))
    res=cursor.fetchone()
    if not res:
        raise HTTPException(status_code=400,detail='User not found')
    return{'Details':res}
