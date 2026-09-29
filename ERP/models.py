from database import get_connection

def criar_tabelas():
    """Cria todas as tabelas do ERP com base no esquema relacional."""
    conn = get_connection()
    cursor = conn.cursor()

    schema = """
    -- ==========================================
    -- BLOCO 1: CADASTROS BASE (DIMENSÕES)
    -- ==========================================

    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        cnpj TEXT UNIQUE,
        razao_social TEXT NOT NULL,
        telefone TEXT,
        email_contato TEXT
    );

    CREATE TABLE IF NOT EXISTS vendedores (
        id_vendedor INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_vendedor TEXT NOT NULL,
        email_vendedor TEXT
    );

    CREATE TABLE IF NOT EXISTS fornecedores (
        id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
        cnpj TEXT UNIQUE,
        nome_fornecedor TEXT NOT NULL,
        nome_contato TEXT
    );

    CREATE TABLE IF NOT EXISTS transportadoras (
        id_transportadora INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_empresa TEXT NOT NULL,
        tipo_veiculo TEXT,
        telefone_contato TEXT
    );

    CREATE TABLE IF NOT EXISTS categorias_produtos (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_categoria TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS produtos (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        id_categoria INTEGER,
        codigo_sku TEXT,
        descricao TEXT NOT NULL,
        url_referencia TEXT,
        FOREIGN KEY (id_categoria) REFERENCES categorias_produtos(id_categoria)
    );

    -- ==========================================
    -- BLOCO 2: O CORAÇÃO DO SISTEMA (VENDAS)
    -- ==========================================

    CREATE TABLE IF NOT EXISTS pedidos (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        id_vendedor INTEGER,
        numero_pedido TEXT NOT NULL,
        data_emissao TEXT NOT NULL,
        status_venda TEXT DEFAULT 'Orçamento',
        valor_total REAL,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY (id_vendedor) REFERENCES vendedores(id_vendedor)
    );

    CREATE TABLE IF NOT EXISTS itens_pedido (
        id_item_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
        FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
    );

    -- ==========================================
    -- BLOCO 3: OPERAÇÃO, LOGÍSTICA E AUDITORIA
    -- ==========================================

    CREATE TABLE IF NOT EXISTS compras (
        id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL,
        id_fornecedor INTEGER NOT NULL,
        nf_compra TEXT,
        valor_custo_item REAL,
        valor_frete_compra REAL,
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
        FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
    );

    CREATE TABLE IF NOT EXISTS logistica_final (
        id_logistica INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL UNIQUE,
        id_transportadora INTEGER,
        nf_venda TEXT,
        codigo_rastreio TEXT,
        data_chegada_base TEXT,
        data_entrega_final TEXT,
        status_logistico TEXT,
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
        FOREIGN KEY (id_transportadora) REFERENCES transportadoras(id_transportadora)
    );

    CREATE TABLE IF NOT EXISTS movimentacoes_financeiras (
        id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER, 
        id_compra INTEGER, 
        tipo_movimentacao TEXT NOT NULL,
        valor REAL NOT NULL,
        data_vencimento TEXT NOT NULL,
        data_pagamento TEXT,
        status_pagamento TEXT DEFAULT 'Pendente',
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
        FOREIGN KEY (id_compra) REFERENCES compras(id_compra)
    );

    CREATE TABLE IF NOT EXISTS historico_pedidos (
        id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL,
        data_hora TEXT DEFAULT CURRENT_TIMESTAMP,
        status_alterado_para TEXT NOT NULL,
        observacao TEXT,
        usuario_responsavel TEXT,
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE
    );
    """

    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Base de dados e tabelas inicializadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()