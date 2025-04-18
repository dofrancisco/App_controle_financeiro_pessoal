from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    valor = Column(Float)
    tipo = Column(String)  # 'receita' ou 'despesa'
    data = Column(DateTime, default=datetime.now)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    
    # Novos campos para recorrência e parcelamento
    is_recorrente = Column(Boolean, default=False)  # Se é uma transação mensal recorrente
    is_parcelada = Column(Boolean, default=False)   # Se é uma transação parcelada
    total_parcelas = Column(Integer, nullable=True)  # Número total de parcelas
    parcela_atual = Column(Integer, nullable=True)   # Número da parcela atual
    data_final = Column(DateTime, nullable=True)     # Data final para transações recorrentes
    
    # Relacionamento com a categoria
    categoria = relationship("Categoria", back_populates="transacoes")