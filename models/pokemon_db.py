# Column define una columna. Los otros son los tipos de dato SQL.
from sqlalchemy import Column, Integer, String, Boolean

# Base viene de database.py. Heredar de ella es lo que le avisa a SQLAlchemy
# que esta clase representa una tabla.
from database import Base


class PokemonDB(Base):
    # Nombre real que va a tener la tabla en MySQL.
    __tablename__ = "pokemon"

    # primary_key=True -> clave primaria. En MySQL, una clave primaria entera
    # es AUTO_INCREMENT por defecto, así que el id lo asigna la base sola.
    # index=True crea un índice para que las búsquedas por id sean rápidas.
    id = Column(Integer, primary_key=True, index=True)

    # String necesita longitud en MySQL: String(50) es VARCHAR(50).
    # nullable=False -> la columna no admite NULL, es obligatoria.
    # unique=True -> no puede haber dos Pokémon con el mismo nombre.
    nombre = Column(String(50), nullable=False, unique=True)

    tipo = Column(String(30), nullable=False)

    nivel = Column(Integer, nullable=False)

    # default=False es el valor que usa la base si no se le manda nada.
    legendario = Column(Boolean, default=False, nullable=False)