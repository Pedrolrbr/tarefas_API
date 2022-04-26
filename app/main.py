from datetime import date
from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn
from app import models
from .database import SessionLocal, engine


app = FastAPI()

#Criar a tabela
models.Base.metadata.create_all(bind=engine)


#Habilitar o CORS
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5500",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Templates
templates = Jinja2Templates(directory="C:/Users/pedro/tarefas_front/templates")



# FUNÇÃO get_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#VER AS TODAS AS TAREFAS
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).all()
    return templates.TemplateResponse("index.html",
                                      {"request": request, "tarefa_list": tarefa})

#ADICIONAR NOVAS TAREFAS
@app.post("/add")
def add(request: Request, dia: str = Form(...), title: str = Form(...), db: Session = Depends(get_db)):
    novo_dia = models.Tarefa(dia=dia)
    nova_tarefa = models.Tarefa(title=title)
    db.add(nova_tarefa, novo_dia)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

#ATUALIZAR OS STATUS DA TAREFFA
@app.get("/update/{tarefa_id}")
def update(request: Request, tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    tarefa.complete = not tarefa.complete
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

#DELETAR UMA TAREFA
@app.get("/delete/{tarefa_id}")
def delete(request: Request, tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    db.delete(tarefa)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

