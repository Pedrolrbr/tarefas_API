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
'''
!!!! ESPECIFICAR O LOCAL DA PASTA tarefas_front !!!!
'''
templates = Jinja2Templates(directory="C:/Users/pedro/tarefas_front/templates")

filtros = Jinja2Templates(directory="C:/Users/pedro/tarefas_front/templates/filtros")



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

#RETORNA TODAS AS TAREFAS
@app.get("/tarefas")
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Tarefa).all() 
    return items


#Tarefas Finalizadas
@app.get("/tarefas_finalizadas")
def get_items_finalizadas(request: Request, db: Session = Depends(get_db)):
    finalizadas = db.query(models.Tarefa).filter(models.Tarefa.complete == '1')
    return filtros.TemplateResponse("finished.html",
                                {"request": request, "tarefa_list": finalizadas})

#TAREFAS ESPORTE
@app.get("/tarefas_esporte")
def get_items_finalizadas(request: Request, db: Session = Depends(get_db)):
    esporte = db.query(models.Tarefa).filter(models.Tarefa.tipo == 'Esportes')
    return filtros.TemplateResponse("esportes.html",
                                {"request": request, "tarefa_list": esporte})                                

#TAREFAS TRABALHO
@app.get("/tarefas_trabalho")
def get_items_finalizadas(request: Request, db: Session = Depends(get_db)):
    trabalho = db.query(models.Tarefa).filter(models.Tarefa.tipo == 'Trabalho')
    return filtros.TemplateResponse("trabalho.html",
                                {"request": request, "tarefa_list": trabalho})

#TAREFAS ESTUDOS
@app.get("/tarefas_estudo")
def get_items_finalizadas(request: Request, db: Session = Depends(get_db)):
    estudo = db.query(models.Tarefa).filter(models.Tarefa.tipo == 'Estudos')
    return filtros.TemplateResponse("estudos.html",
                                {"request": request, "tarefa_list": estudo})          


#TAREFAS LAZER
@app.get("/tarefas_lazer")
def get_items_finalizadas(request: Request, db: Session = Depends(get_db)):
    lazer = db.query(models.Tarefa).filter(models.Tarefa.tipo == 'Lazer')
    return filtros.TemplateResponse("lazer.html",
                                {"request": request, "tarefa_list": lazer})   

#TAREFAS VIAGEM
@app.get("/tarefas_viagem")
def get_items_finalizadas(request: Request, db: Session = Depends(get_db)):
    viagem = db.query(models.Tarefa).filter(models.Tarefa.tipo == 'Viagem')
    return filtros.TemplateResponse("viagem.html",
                                {"request": request, "tarefa_list": viagem})   



#ADICIONAR NOVAS TAREFAS
@app.post("/add")
def add(request: Request, tipo: str = Form(...), dia: str = Form(...), title: str = Form(...), db: Session = Depends(get_db)):
    nova_tarefa = models.Tarefa(title=title, dia=dia, tipo=tipo)
    db.add(nova_tarefa)
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

