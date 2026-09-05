# Depends es la novedad de este archivo: sirve para inyectar dependencias.
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from models.pokemon import Pokemon, PokemonBase
from services import pokemon_service
# get_db es la función de database.py que abre y cierra la sesión.
from database import get_db

router = APIRouter(prefix="/pokemon", tags=["Pokémon"])


# GET /pokemon
# db: Session = Depends(get_db) es la línea nueva respecto al proyecto anterior.
# Antes de ejecutar la función, FastAPI llama a get_db(), toma la sesión que
# entrega el yield y la pasa en el parámetro db. Cuando la función termina,
# vuelve a get_db() y ejecuta el finally que la cierra.
# Resultado: cada request tiene su propia sesión y siempre se cierra sola.
@router.get("", response_model=list[Pokemon])
def listar(db: Session = Depends(get_db)):
    return pokemon_service.listar_todos(db)


# GET /pokemon/{pokemon_id}
# Dos parámetros de origen distinto: pokemon_id viene de la URL (está entre
# llaves en la ruta), db viene de la dependencia. FastAPI lo resuelve solo.
@router.get("/{pokemon_id}", response_model=Pokemon)
def obtener(pokemon_id: int, db: Session = Depends(get_db)):
    resultado = pokemon_service.buscar_por_id(db, pokemon_id)

    # Acá se traduce el None del service a un error HTTP.
    if resultado is None:
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")

    return resultado


# POST /pokemon
# datos es un modelo de Pydantic, así que FastAPI lo toma del body como JSON.
# status_code=201 es el código correcto para "recurso creado".
@router.post("", response_model=Pokemon, status_code=201)
def crear(datos: PokemonBase, db: Session = Depends(get_db)):
    return pokemon_service.crear(db, datos)