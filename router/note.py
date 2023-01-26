from fastapi import APIRouter,Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWSError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import mysql.connector

router = APIRouter()

SECRET ="a09e1d18327ec0c6af21fc942e72a8be1466af605a3791539035a2858d1ab427"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="nota")


class Añadir_nota(BaseModel):
    note_title: str
    note_content: str

class Mostrar_nota(BaseModel):
    id: int
    note_title: str
    note_content: str

class Editar_nota(BaseModel):
    id: int
    note_title: str
    note_content: str

class Eliminar_nota(BaseModel):
    id: int


def get_db():
    cnx = mysql.connector.connect(
        host="sql859.main-hosting.eu",
        user="u362449495_api_notas_user",
        password="/6Net$+B5Py",
        database="u362449495_api_notas"
    )
    return cnx

#retorna el usuario dueño del token
async def current_user(token: str = Depends(oauth2_scheme)):
    email = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")                       
    return email


@router.post("/nota/añadir")
async def Add_note(form_data: Añadir_nota  , db: mysql.connector = Depends(get_db), user = Depends(current_user)):
    
    cursor = db.cursor() 
    query = "INSERT INTO notes (user_email, note_title, note_content) VALUES (%s, %s, %s)"
    values = ( user, form_data.note_title, form_data.note_content )
    cursor.execute(query, values)    
    db.commit()

    return {"nota añadida":True}


@router.get("/nota/mostrar")
async def Show_note( db: mysql.connector = Depends(get_db), user = Depends(current_user)):

    cursor = db.cursor() 
    query = "SELECT id, user_email, note_title, note_content FROM notes WHERE user_email = %s"
    values = (user,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    notas = []
    for row in result:
        nota = Mostrar_nota(id=row[0], note_title=row[2], note_content=row[3])
        notas.append(nota)

    return notas
    

@router.put("/nota/editar")
async def Edit_note( form_data: Editar_nota, db: mysql.connector = Depends(get_db), user = Depends(current_user)):

    cursor = db.cursor()
    query = "UPDATE notes SET note_title = %s, note_content = %s WHERE id = %s and user_email = %s"
    values = (form_data.note_title, form_data.note_content, form_data.id, user)
    cursor.execute(query, values)    
    db.commit()

    return {"nota editada":True}
    
        
@router.delete("/nota/eliminar")
async def Delete_note( form_data: Eliminar_nota, db: mysql.connector = Depends(get_db), user = Depends(current_user)):
    
    cursor = db.cursor()
    query = "DELETE FROM notes WHERE id = %s and user_email = %s"
    values = (form_data.id, user)
    cursor.execute(query, values)  
    db.commit()
    

    return {"nota eliminada":True}