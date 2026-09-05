# Session es el tipo de la sesión de SQLAlchemy. Se usa para tipar el parámetro.
from sqlalchemy.orm import Session

# El modelo de tabla: con esto se hacen las consultas.
from models.pokemon_db import PokemonDB
# El modelo de entrada de Pydantic: es lo que llega desde el controller.
from models.pokemon import PokemonBase


# Ojo: ya no hay lista _pokedex. Los datos ahora viven en MySQL.
# Todas las funciones reciben la sesión (db) como primer parámetro:
# el service no la crea, se la pasa el controller.


def listar_todos(db: Session) -> list[PokemonDB]:
    """Trae todos los Pokémon de la tabla.
    query() arma la consulta, all() la ejecuta y devuelve una lista."""
    return db.query(PokemonDB).all()


def buscar_por_id(db: Session, pokemon_id: int) -> PokemonDB | None:
    """Busca un Pokémon por id.
    filter() agrega el WHERE, first() trae el primer resultado o None.
    Devuelve None si no existe: la traducción a 404 la hace el controller."""
    return db.query(PokemonDB).filter(PokemonDB.id == pokemon_id).first()


def crear(db: Session, datos: PokemonBase) -> PokemonDB:
    """Crea un Pokémon nuevo en la base."""
    # model_dump() convierte el modelo de Pydantic a diccionario,
    # y el ** lo desarma en argumentos: nombre=..., tipo=..., etc.
    # No pasamos id: lo genera MySQL con el auto-incremento.
    nuevo = PokemonDB(**datos.model_dump())

    # Los tres pasos del alta, en orden:
    db.add(nuevo)       # marca el objeto para insertar
    db.commit()         # ejecuta el INSERT de verdad y confirma
    db.refresh(nuevo)   # relee el objeto desde la base para traer el id asignado

    return nuevo