import os

def load(metrics, output_dir='ETL/output'):
    # Cria a pasta se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Salvar DataFrames em CSV
    metrics['df_full'].to_csv(f'{output_dir}/df_full.csv', index=False)
    metrics['receita_diaria'].to_csv(f'{output_dir}/receita_diaria.csv', index=False)
    metrics['total_categoria'].to_csv(f'{output_dir}/total_categoria.csv', index=False)
    metrics['ticket_medio'].to_csv(f'{output_dir}/ticket_medio.csv', index=False)
    metrics['top_clientes'].to_csv(f'{output_dir}/top_clientes.csv', index=False)

    print(f"Todos os arquivos salvos em {output_dir}")

# Teste rápido
if __name__ == "__main__":
    from extract import extract
    from transform import transform

    produtos, clientes, vendas = extract()
    metrics = transform(produtos, clientes, vendas)
    load(metrics)
