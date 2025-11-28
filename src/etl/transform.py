import pandas as pd

def transform(df_produtos, df_clientes, df_vendas):
    # -------------------------
    # 1. Limpeza básica
    # -------------------------
    df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])
    df_vendas = df_vendas[df_vendas['quantidade'] > 0]
    df_vendas = df_vendas[df_vendas['valor_total'] > 0]

    # -------------------------
    # 2. Merge das tabelas
    # -------------------------
    df_full = df_vendas.merge(df_produtos, left_on='produto_id', right_on='id_produto') \
                       .merge(df_clientes, left_on='cliente_id', right_on='id_cliente')

    # -------------------------
    # 3. Métricas básicas
    # -------------------------
    # Receita diária
    receita_diaria = df_full.groupby('data_venda')['valor_total'].sum().reset_index()
    receita_diaria.rename(columns={'valor_total': 'receita_diaria'}, inplace=True)

    # Total por categoria
    total_categoria = df_full.groupby('categoria')['valor_total'].sum().reset_index()
    total_categoria.rename(columns={'valor_total': 'total_categoria'}, inplace=True)

    # Ticket médio por cliente
    ticket_medio = df_full.groupby('id_cliente')['valor_total'].mean().reset_index()
    ticket_medio.rename(columns={'valor_total': 'ticket_medio'}, inplace=True)

    # Top clientes (por receita total)
    top_clientes = df_full.groupby(['id_cliente', 'nome_y'])['valor_total'].sum().reset_index()
    top_clientes.rename(columns={'valor_total': 'total_gasto', 'nome_y': 'nome_cliente'}, inplace=True)
    top_clientes = top_clientes.sort_values(by='total_gasto', ascending=False).head(10)

    # -------------------------
    # Retornar tudo
    # -------------------------
    metrics = {
        'df_full': df_full,
        'receita_diaria': receita_diaria,
        'total_categoria': total_categoria,
        'ticket_medio': ticket_medio,
        'top_clientes': top_clientes
    }

    return metrics

# -------------------------
# Teste do script
# -------------------------
if __name__ == "__main__":
    from extract import extract
    df_produtos, df_clientes, df_vendas = extract()
    metrics = transform(df_produtos, df_clientes, df_vendas)

    print("Transformação e métricas concluídas")
    print("Receita diária:")
    print(metrics['receita_diaria'].head())
    print("\nTotal por categoria:")
    print(metrics['total_categoria'])
    print("\nTicket médio:")
    print(metrics['ticket_medio'].head())
    print("\nTop clientes:")
    print(metrics['top_clientes'])
