from fastapi import APIRouter,Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWSError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import mysql.connector

ALGORITHM = "!!!!"
ACCESS_TOKEN_DURATION = !!!!
SECRET ="!!!!"

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    email: str
    fullname: str
    username: str

class logeo_data(BaseModel):
    email: str
    password: str 

def get_db():
    cnx = mysql.connector.connect(
        host="!!!!",
        user="!!!!",
        password="!!!!",
        database="!!!!"
    )
    return cnx

#funcion para el  login
async def read_db(db: mysql.connector = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()    
    columns = [col[0] for col in cursor.description] 
    data_objects = []  
    for row in data:
        data_object = {columns[i]: row[i] for i in range(len(columns))}
        data_objects.append(data_object)
    return data_objects

#funcion para validar que estas conectado
async def current_user(token: str = Depends(oauth2_scheme)):
    try:
        email = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="no estamos autorizados")
    except JWSError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="no estamos autorizados")    
    return email

@router.post("/login")
async def login( form_data: logeo_data, data_objects = Depends(read_db)):
    email = form_data.email    
    correo_validado = False

    for correo in data_objects:
        if correo["email"] == email:
            correo_validado = True
            data_usuario = correo

    if  correo_validado != True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="el correo no se encuentra registrado")
    if not crypt.verify(form_data.password, data_usuario["password"]): 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="la contraseña no es correcta")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {"sub":form_data.email, "exp":expire, }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer", "time_expire":ACCESS_TOKEN_DURATION}

@router.get("/users/me")
async def me(user = Depends(current_user), data_objects = Depends(read_db)):
     for correo in data_objects:
        if correo["email"] == user:                        
            return User(**correo)
