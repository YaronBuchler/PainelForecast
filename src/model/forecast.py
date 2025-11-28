import sys
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Adicionar src ao path para importar ETL
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_forecast(receita_diaria, dias_previsao=30):
    df = receita_diaria.copy()

    # Garantir que data_venda é datetime
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df = df.dropna(subset=['data_venda', 'receita_diaria'])
    df = df.sort_values('data_venda')

    # Criar índice do dia para regressão
    df['dia_num'] = (df['data_venda'] - df['data_venda'].min()).dt.days.astype(int)

    X = df[['dia_num']]
    y = df['receita_diaria']

    # Treinar modelo de regressão linear
    model = LinearRegression()
    model.fit(X, y)

    # Criar previsão para os próximos dias
    ultimo_dia = df['dia_num'].max()
    dias_futuros = np.arange(ultimo_dia + 1, ultimo_dia + dias_previsao + 1).reshape(-1, 1)
    previsao = model.predict(dias_futuros)

    # Garantir que valores negativos sejam 0
    previsao = np.clip(previsao, 0, None)

    datas_futuras = [df['data_venda'].max() + pd.Timedelta(days=i) for i in range(1, dias_previsao + 1)]
    df_forecast = pd.DataFrame({
        'data_venda': datas_futuras,
        'receita_prevista': previsao
    })

    # -------------------------
    # Salvar CSV fixo no caminho correto
    # -------------------------
    output_dir = r"C:\Users\Aluno\Desktop\projeto\ETL\output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'forecast_30dias_test.csv')

    print("Primeiras linhas do forecast antes de salvar:")
    print(df_forecast.head())
    print(f"Salvando forecast em: {output_path}")

    df_forecast.to_csv(output_path, index=False)

    return df_forecast

# -------------------------
# Teste rápido
# -------------------------
if __name__ == "__main__":
    from etl.extract import extract
    from etl.transform import transform

    produtos, clientes, vendas = extract()
    metrics = transform(produtos, clientes, vendas)
    forecast = run_forecast(metrics['receita_diaria'])
