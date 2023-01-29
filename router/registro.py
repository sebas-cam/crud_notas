from fastapi import APIRouter,Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt, JWSError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import mysql.connector

router = APIRouter()
crypt = CryptContext(schemes=["bcrypt"])

#base que se envia por el body para crear el usuario
class registro_data(BaseModel):
    email: str
    password: str 
    fullname: str
    username: str

def get_db():
    cnx = mysql.connector.connect(
        host="!!!!",
        user="!!!!",
        password="!!!!",
        database="!!!!"
    )
    return cnx

async def valid_email(form_data: registro_data, db: mysql.connector = Depends(get_db)):
    email = form_data.email
    cursor = db.cursor() 
    cursor.execute('SELECT email FROM user')
    emails = cursor.fetchall()   
    emails = [i[0] for i in emails]
    return any(elem == email for elem in emails)    

@router.post("/registro")
async def registro(form_data: registro_data  , db: mysql.connector = Depends(get_db), email_valid = Depends(valid_email) ):
    
    if email_valid == True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="el email ya fue usado")        
        
    cursor = db.cursor()    
    query = "INSERT INTO user (email, fullname, password, username) VALUES (%s, %s, %s, %s)"
    
    code_password = crypt.encrypt(form_data.password)

    values = ( form_data.email, form_data.fullname, code_password, form_data.username )
    cursor.execute(query, values)
    db.commit()  
    return {"detail":"correcto"}
