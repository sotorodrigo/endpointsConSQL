# create_engine: crea el motor, el objeto que sabe hablar con MySQL.
from sqlalchemy import create_engine
# declarative_base: fabrica la clase de la que heredan los modelos de tabla.
# sessionmaker: fábrica de sesiones (cada sesión es una conversación con la base).
from sqlalchemy.orm import declarative_base, sessionmaker


# La URL de conexión. Formato:
# dialecto+driver://usuario:contraseña@host:puerto/nombre_del_esquema
#
#   mysql+pymysql  -> MySQL usando el driver pymysql que instalaste
#   root           -> tu usuario
#   TU_PASSWORD    -> reemplazá por la contraseña que pusiste al instalar MySQL
#   localhost:3306 -> la base corre en tu propia máquina, puerto por defecto
#   pokedex_db     -> el esquema que creaste en Workbench
DATABASE_URL = "mysql+pymysql://root:utn12345@localhost:3306/pokedex_db"


# El engine mantiene un pool de conexiones abiertas y las reutiliza.
# Se crea UNA sola vez en toda la aplicación.
# echo=True imprime en consola cada SQL que se ejecuta: muy útil para aprender,
# después lo podés poner en False.
engine = create_engine(DATABASE_URL, echo=True)


# Fábrica de sesiones. Cada request va a pedir una sesión nueva a esta fábrica.
# autoflush=False evita que SQLAlchemy mande cambios a la base antes de tiempo.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Clase base. Todos los modelos de tabla van a heredar de acá,
# y así SQLAlchemy sabe qué tablas tiene que manejar.
Base = declarative_base()


# Dependencia para FastAPI: abre una sesión, se la presta al endpoint,
# y la cierra siempre al terminar (aunque haya error, por el finally).
# El yield es lo que la convierte en dependencia: entrega el valor y
# retoma la ejecución cuando el endpoint termina.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()