from typing import Union
from fastapi import FastAPI
from router import registro, jwt_autenticacion, note

app = FastAPI()

#iniciar servido = python -m uvicorn main:app --reload
#documentacion = url + /docs o /redoc

app.include_router(registro.router)
app.include_router(jwt_autenticacion.router)
app.include_router(note.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

#documentacion http://127.0.0.1:8000/docs