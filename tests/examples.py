from models.database import SessionLocal
from models.categoria import Categoria
from models.transacao import Transacao
from datetime import datetime

# Criar uma sessão do banco de dados
db = SessionLocal()

# 1. Criar categorias
def criar_categorias():
    categorias = [
        Categoria(nome="Salário", tipo="receita", descricao="Rendimentos mensais"),
        Categoria(nome="Alimentação", tipo="despesa", descricao="Gastos com comida"),
        Categoria(nome="Transporte", tipo="despesa", descricao="Gastos com transporte"),
    ]
    
    for categoria in categorias:
        db.add(categoria)
    db.commit()
    print("Categorias criadas com sucesso!")

# 2. Adicionar uma transação
def adicionar_transacao(descricao, valor, tipo, categoria_nome):
    # Buscar categoria
    categoria = db.query(Categoria).filter(Categoria.nome == categoria_nome).first()
    if not categoria:
        print(f"Categoria {categoria_nome} não encontrada!")
        return
    
    # Criar transação
    transacao = Transacao(
        descricao=descricao,
        valor=valor,
        tipo=tipo,
        categoria_id=categoria.id,
        data=datetime.now()
    )
    
    db.add(transacao)
    db.commit()
    print("Transação registrada com sucesso!")

# 3. Listar todas as transações
def listar_transacoes():
    transacoes = db.query(Transacao).all()
    for t in transacoes:
        categoria = db.query(Categoria).filter(Categoria.id == t.categoria_id).first()
        print(f"Data: {t.data.strftime('%d/%m/%Y')}")
        print(f"Descrição: {t.descricao}")
        print(f"Valor: R$ {t.valor:.2f}")
        print(f"Tipo: {t.tipo}")
        print(f"Categoria: {categoria.nome}")
        print("-" * 30)

# 4. Calcular saldo
def calcular_saldo():
    transacoes = db.query(Transacao).all()
    saldo = 0
    
    for t in transacoes:
        if t.tipo == "receita":
            saldo += t.valor
        else:
            saldo -= t.valor
    
    print(f"Saldo atual: R$ {saldo:.2f}")

# Exemplo de uso:
if __name__ == "__main__":
    # Criar categorias iniciais
    criar_categorias()
    
    # Adicionar algumas transações
    adicionar_transacao("Salário mensal", 5000.00, "receita", "Salário")
    adicionar_transacao("Almoço", 25.90, "despesa", "Alimentação")
    adicionar_transacao("Uber", 18.50, "despesa", "Transporte")
    
    # Listar todas as transações
    print("\nLista de Transações:")
    listar_transacoes()
    
    # Mostrar saldo
    print("\nSaldo:")
    calcular_saldo()