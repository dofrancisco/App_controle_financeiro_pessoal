from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    tipo = Column(String)  # 'receita' ou 'despesa'
    descricao = Column(String, nullable=True)
    
    # Adicionar o relacionamento com transações
    transacoes = relationship("Transacao", back_populates="categoria")