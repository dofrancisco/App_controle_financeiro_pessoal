from .database import Base, engine, get_db
from .categoria import Categoria
from .transacao import Transacao

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)