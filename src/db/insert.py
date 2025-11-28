import random
from datetime import datetime, timedelta
from connection import get_connection  # importa a função de conexão

# -------------------------
# Conexão com o banco
# -------------------------
conn = get_connection()
cursor = conn.cursor()

# -------------------------
# Produtos
# -------------------------
produtos = [
    ('Produto A', 'Categoria 1', 10.0),
    ('Produto B', 'Categoria 2', 20.0),
    ('Produto C', 'Categoria 1', 15.0),
    ('Produto D', 'Categoria 3', 50.0),
    ('Produto E', 'Categoria 2', 30.0)
]

for i, (nome, categoria, preco) in enumerate(produtos, start=1):
    cursor.execute(
        "INSERT INTO produtos (id_produto, nome, categoria, preco_unitario) VALUES (?, ?, ?, ?)",
        (i, nome, categoria, preco)
    )

# -------------------------
# Clientes
# -------------------------
cidades = ['São Paulo', 'Rio de Janeiro', 'Curitiba', 'Porto Alegre']
segmentos = ['Varejo', 'Atacado', 'Online']

clientes = []
for i in range(1, 21):  # 20 clientes
    nome = f'Cliente {i}'
    cidade = random.choice(cidades)
    segmento = random.choice(segmentos)
    clientes.append((i, nome, cidade, segmento))
    cursor.execute(
        "INSERT INTO clientes (id_cliente, nome, cidade, segmento) VALUES (?, ?, ?, ?)",
        (i, nome, cidade, segmento)
    )

# -------------------------
# Vendas
# -------------------------
data_inicio = datetime(2025, 1, 1)
num_vendas = 100

for _ in range(num_vendas):
    cliente_id = random.randint(1, len(clientes))
    produto_id = random.randint(1, len(produtos))
    quantidade = random.randint(1, 5)
    data_venda = data_inicio + timedelta(days=random.randint(0, 180))

    # Pegar preço do produto
    cursor.execute("SELECT preco_unitario FROM produtos WHERE id_produto=?", (produto_id,))
    preco_unitario = cursor.fetchone()[0]
    valor_total = quantidade * preco_unitario

    cursor.execute(
        "INSERT INTO vendas (cliente_id, produto_id, data_venda, quantidade, valor_total) VALUES (?, ?, ?, ?, ?)",
        (cliente_id, produto_id, data_venda.strftime('%Y-%m-%d'), quantidade, valor_total)
    )

# -------------------------
# Commit e fechar conexão
# -------------------------
conn.commit()
conn.close()
print("Dados inseridos com sucesso!")
