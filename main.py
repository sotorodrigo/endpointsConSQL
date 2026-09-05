from fastapi import FastAPI

from database import Base, engine
from controllers import pokemon_controller

# IMPORTANTE: hay que importar el modelo de tabla aunque acá no se use.
# Base solo conoce las clases que fueron importadas alguna vez; si este
# import falta, create_all no encuentra la tabla y no crea nada.
from models import pokemon_db  # noqa: F401


app = FastAPI(title="Pokédex API")


# Crea en MySQL las tablas que todavía no existan.
# Si la tabla ya está, no la toca ni la modifica.
# Sirve para aprender; en un proyecto real esto se hace con migraciones (Alembic).
Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Home"])
def home():
    return {"mensaje": "Pokédex API funcionando"}


app.include_router(pokemon_controller.router)