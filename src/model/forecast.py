import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

def run_forecast(receita_diaria, dias_previsao=30):
    """
    Recebe receita_diaria (DataFrame com data_venda e receita_diaria)
    e retorna um DataFrame com forecast dos próximos dias.
    """
    df = receita_diaria.copy()

    # Garantir que data_venda é datetime e remover linhas inválidas
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df = df.dropna(subset=['data_venda', 'receita_diaria'])
    df = df.sort_values('data_venda')

    # Criar variável para regressão
    df['dia_num'] = (df['data_venda'] - df['data_venda'].min()).dt.days.astype(int)

    X = df[['dia_num']]
    y = df['receita_diaria']

    # Treinar modelo
    model = LinearRegression()
    model.fit(X, y)

    # Previsão para os próximos dias
    ultimo_dia = df['dia_num'].max()
    dias_futuros = np.arange(ultimo_dia + 1, ultimo_dia + dias_previsao + 1).reshape(-1, 1)
    previsao = model.predict(dias_futuros)
    previsao = np.clip(previsao, 0, None)  # sem valores negativos

    # Criar datas futuras
    datas_futuras = [df['data_venda'].max() + pd.Timedelta(days=i) for i in range(1, dias_previsao + 1)]
    df_forecast = pd.DataFrame({
        'data_venda': datas_futuras,
        'receita_prevista': previsao
    })

    # Retorna apenas o DataFrame, sem salvar CSV
    return df_forecast
