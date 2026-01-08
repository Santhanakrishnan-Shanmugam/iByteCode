from fastapi import APIRouter,HTTPException

from DB import getConnection
router=APIRouter()



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
