from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Obtener las variables de entorno
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_DATABASE = getenv("DB_DATABASE")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_SSL = getenv("DB_SSL", "false").lower() == "true"

# Construir la URL de conexión
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# Configurar SSL si está habilitado
connect_args = {}
if DB_SSL:
    connect_args["sslmode"] = "require"

# Crear el engine con la configuración
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 