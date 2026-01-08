from fastapi import APIRouter,HTTPException
from router.create_router import user
from models import Del
from DB import getConnection
router=APIRouter()

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
