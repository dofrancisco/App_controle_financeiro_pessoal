import streamlit as st
from models.database import SessionLocal
from models.categoria import Categoria
from models.transacao import Transacao
from datetime import datetime, timedelta
import pandas as pd

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def remover_transacao(transacao_id):
    db = get_db()
    transacao = db.query(Transacao).filter(Transacao.id == transacao_id).first()
    if transacao:
        db.delete(transacao)
        db.commit()
        return True
    return False

def criar_categoria_padrao():
    db = get_db()
    # Verifica se já existem categorias
    if db.query(Categoria).first() is None:
        categorias_padrao = [
            Categoria(nome="Salário", tipo="receita", descricao="Rendimentos mensais"),
            Categoria(nome="Alimentação", tipo="despesa", descricao="Gastos com comida"),
            Categoria(nome="Transporte", tipo="despesa", descricao="Gastos com transporte"),
            Categoria(nome="Lazer", tipo="despesa", descricao="Gastos com entretenimento"),
            Categoria(nome="Outros", tipo="despesa", descricao="Gastos diversos"),
        ]
        for categoria in categorias_padrao:
            db.add(categoria)
        db.commit()

def adicionar_transacao(descricao, valor, tipo, categoria_nome, data, is_recorrente=False, 
                       is_parcelada=False, total_parcelas=None, data_final=None):
    db = get_db()
    categoria = db.query(Categoria).filter(Categoria.nome == categoria_nome).first()
    
    if is_parcelada:
        # Calcular valor por parcela
        valor_parcela = valor / total_parcelas
        
        # Criar uma transação para cada parcela
        for i in range(total_parcelas):
            data_parcela = data + timedelta(days=30 * i)  # Adiciona 30 dias para cada parcela
            transacao = Transacao(
                descricao=f"{descricao} ({i+1}/{total_parcelas})",
                valor=valor_parcela,
                tipo=tipo,
                categoria_id=categoria.id,
                data=data_parcela,
                is_parcelada=True,
                total_parcelas=total_parcelas,
                parcela_atual=i+1
            )
            db.add(transacao)
    
    elif is_recorrente:
        # Criar transações recorrentes até a data final
        data_atual = data
        while data_atual <= data_final:
            transacao = Transacao(
                descricao=descricao,
                valor=valor,
                tipo=tipo,
                categoria_id=categoria.id,
                data=data_atual,
                is_recorrente=True,
                data_final=data_final
            )
            db.add(transacao)
            data_atual = data_atual + timedelta(days=30)  # Adiciona 30 dias para próxima recorrência
    
    else:
        # Transação única normal
        transacao = Transacao(
            descricao=descricao,
            valor=valor,
            tipo=tipo,
            categoria_id=categoria.id,
            data=data
        )
        db.add(transacao)
    
    db.commit()

def listar_transacoes():
    db = get_db()
    transacoes = db.query(Transacao).all()
    
    dados = []
    for t in transacoes:
        categoria = db.query(Categoria).filter(Categoria.id == t.categoria_id).first()
        dados.append({
            "Data": t.data.strftime("%d/%m/%Y"),
            "Descrição": t.descricao,
            "Valor": f"R$ {t.valor:.2f}",
            "Tipo": t.tipo.capitalize(),
            "Categoria": categoria.nome
        })
    
    return dados

def calcular_saldo():
    db = get_db()
    transacoes = db.query(Transacao).all()
    receitas = sum(t.valor for t in transacoes if t.tipo == "receita")
    despesas = sum(t.valor for t in transacoes if t.tipo == "despesa")
    return receitas, despesas, receitas - despesas

def main():
    st.set_page_config(page_title="Controle Financeiro", layout="wide")
    
    # Criar categorias padrão se não existirem
    criar_categoria_padrao()
    
    # Título principal
    st.title("💰 Controle Financeiro Pessoal")
    
    # Menu lateral
    st.sidebar.title("Menu")
    pagina = st.sidebar.radio("Navegação", ["Dashboard", "Nova Transação", "Histórico"])
    
    if pagina == "Dashboard":
        # Mostrar saldo
        receitas, despesas, saldo = calcular_saldo()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Receitas", f"R$ {receitas:.2f}", delta=None)
        with col2:
            st.metric("Despesas", f"R$ {despesas:.2f}", delta=None)
        with col3:
            st.metric("Saldo", f"R$ {saldo:.2f}", 
                     delta="positivo" if saldo >= 0 else "negativo")
        
        # Mostrar últimas transações
        st.subheader("Últimas Transações")
        dados = listar_transacoes()
        if dados:
            df = pd.DataFrame(dados)
            st.dataframe(df)
        else:
            st.info("Nenhuma transação registrada ainda.")
            
    elif pagina == "Nova Transação":
        st.header("📝 Nova Transação")
        
        with st.form("nova_transacao", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                descricao = st.text_input("Descrição")
                valor = st.number_input("Valor", min_value=0.0, format="%.2f")
                data = st.date_input("Data", datetime.now())
                
            with col2:
                tipo = st.selectbox("Tipo", ["receita", "despesa"])
                db = get_db()
                categorias = db.query(Categoria).filter(Categoria.tipo == tipo).all()
                categoria = st.selectbox("Categoria", [c.nome for c in categorias])
            
            # Opções de recorrência e parcelamento
            tipo_transacao = st.radio("Tipo de Transação", 
                                    ["Única", "Recorrente Mensal", "Parcelada"])
            
            if tipo_transacao == "Recorrente Mensal":
                data_final = st.date_input("Data Final da Recorrência", 
                                         min_value=data,
                                         value=data + timedelta(days=365))  # 1 ano por padrão
                is_recorrente = True
                is_parcelada = False
                total_parcelas = None
            
            elif tipo_transacao == "Parcelada":
                total_parcelas = st.number_input("Número de Parcelas", 
                                               min_value=2, 
                                               max_value=48,  # máximo 48 parcelas
                                               value=12)
                is_recorrente = False
                is_parcelada = True
                data_final = None
            
            else:  # Única
                is_recorrente = False
                is_parcelada = False
                total_parcelas = None
                data_final = None
            
            submitted = st.form_submit_button("Adicionar Transação")
            
            if submitted:
                try:
                    adicionar_transacao(
                        descricao=descricao,
                        valor=valor,
                        tipo=tipo,
                        categoria_nome=categoria,
                        data=data,
                        is_recorrente=is_recorrente,
                        is_parcelada=is_parcelada,
                        total_parcelas=total_parcelas,
                        data_final=data_final
                    )
                    st.success("Transação(ões) adicionada(s) com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar transação: {str(e)}")

    elif pagina == "Histórico":
        st.header("📊 Histórico de Transações")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            tipo_filtro = st.selectbox("Filtrar por tipo", ["Todos", "Receita", "Despesa"])
        with col2:
            db = get_db()
            categorias = ["Todas"] + [c.nome for c in db.query(Categoria).all()]
            categoria_filtro = st.selectbox("Filtrar por categoria", categorias)
        with col3:
            tipo_transacao_filtro = st.selectbox(
                "Tipo de Transação",
                ["Todas", "Únicas", "Recorrentes", "Parceladas"]
            )
        
        # Buscar transações
        db = get_db()
        transacoes = db.query(Transacao).all()
        
        if transacoes:
            for transacao in transacoes:
                # Aplicar filtros
                if tipo_filtro != "Todos" and tipo_filtro.lower() != transacao.tipo:
                    continue
                    
                categoria = db.query(Categoria).filter(Categoria.id == transacao.categoria_id).first()
                if categoria_filtro != "Todas" and categoria_filtro != categoria.nome:
                    continue
                    
                if tipo_transacao_filtro == "Únicas" and (transacao.is_recorrente or transacao.is_parcelada):
                    continue
                elif tipo_transacao_filtro == "Recorrentes" and not transacao.is_recorrente:
                    continue
                elif tipo_transacao_filtro == "Parceladas" and not transacao.is_parcelada:
                    continue
                
                # Exibir transação
                with st.container():
                    col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 1.5, 1, 1.5, 1])
                    
                    with col1:
                        st.write(transacao.data.strftime("%d/%m/%Y"))
                    with col2:
                        desc = transacao.descricao
                        if transacao.is_parcelada:
                            desc += f" ({transacao.parcela_atual}/{transacao.total_parcelas})"
                        elif transacao.is_recorrente:
                            desc += " (Recorrente)"
                        st.write(desc)
                    with col3:
                        valor_texto = f"R$ {transacao.valor:.2f}"
                        if transacao.tipo == "receita":
                            st.markdown(f"<span style='color:green'>{valor_texto}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<span style='color:red'>{valor_texto}</span>", unsafe_allow_html=True)
                    with col4:
                        st.write(transacao.tipo.capitalize())
                    with col5:
                        st.write(categoria.nome)
                    with col6:
                        if st.button("🗑️", key=f"remove_{transacao.id}"):
                            if remover_transacao(transacao.id):
                                st.success("Transação removida!")
                                st.rerun()
                            else:
                                st.error("Erro ao remover.")
                    
                    st.markdown("---")
        else:
            st.info("Nenhuma transação registrada ainda.")

if __name__ == "__main__":
    main()