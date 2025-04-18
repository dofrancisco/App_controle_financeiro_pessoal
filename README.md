# App de Controle Financeiro Pessoal

## Descrição
Aplicativo para controle financeiro pessoal, permitindo ao usuário registrar receitas, despesas, categorizar transações, visualizar relatórios e acompanhar o saldo.

## Funcionalidades Principais
- Cadastro de receitas e despesas
- Categorias personalizáveis
- Relatórios e gráficos de gastos/receitas
- Saldo atualizado automaticamente
- Filtros por período, categoria, tipo de transação
- Exportação de dados (CSV, PDF)
- Autenticação de usuário (opcional)

## Estrutura de Pastas Sugerida
```
/ (raiz)
│
├── src/                # Código-fonte principal
│   ├── models/         # Modelos de dados (ex: Transacao, Categoria, Usuario)
│   ├── controllers/    # Lógica de negócio e manipulação dos dados
│   ├── services/       # Serviços auxiliares (ex: exportação, autenticação)
│   ├── views/          # Interface com Streamlit
│   └── utils/          # Funções utilitárias
│
├── tests/              # Testes automatizados
│
├── docs/               # Documentação adicional
│
├── requirements.txt    # Dependências do projeto (Python)
└── README.md           # Documentação principal
```

## Tecnologias Utilizadas
- Backend e lógica: Python 3.x
- Frontend: Streamlit
- Banco de dados: SQLite (padrão, pode ser trocado por outro)

## Próximos Passos
1. Inicializar o projeto Python e criar o arquivo requirements.txt
2. Definir os modelos principais (Transacao, Categoria, Usuario)
3. Implementar a interface inicial com Streamlit para cadastro e listagem de transações
4. Adicionar funcionalidades de relatório e filtros
5. Escrever testes básicos para as principais funções 