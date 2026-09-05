from pydantic import BaseModel, ConfigDict


# Modelo de ENTRADA: lo que manda el cliente en el body de un POST o PUT.
# No lleva id porque ese lo genera MySQL con el auto-incremento.
class PokemonBase(BaseModel):
    nombre: str
    tipo: str
    nivel: int
    legendario: bool = False


# Modelo de SALIDA: lo que la API devuelve. Suma el id.
class Pokemon(PokemonBase):
    id: int

    # Esta línea es la única novedad respecto al proyecto anterior, y es clave.
    # Por defecto Pydantic solo sabe leer diccionarios. Con from_attributes=True
    # aprende a leer también objetos, tomando sus atributos.
    # Eso le permite convertir un PokemonDB (objeto de SQLAlchemy) en un
    # Pokemon (modelo de Pydantic) automáticamente, sin que vos copies
    # campo por campo.
    model_config = ConfigDict(from_attributes=True)