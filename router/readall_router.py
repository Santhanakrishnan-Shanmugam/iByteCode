from fastapi import APIRouter
from typing import Optional
from DB import getConnection

router = APIRouter()

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
