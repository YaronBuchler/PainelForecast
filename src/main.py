import sys
import os

# -------------------------
# Ajuste de caminhos para importar ETL e model
# -------------------------
base_path = os.path.dirname(__file__)
sys.path.append(os.path.join(base_path, 'etl'))
sys.path.append(os.path.join(base_path, 'model'))

# -------------------------
# Importar módulos
# -------------------------
from extract import extract
from transform import transform
from load import load

# -------------------------
# 1. Extração
# -------------------------
print("Iniciando ETL: extração de dados...")
produtos, clientes, vendas = extract()
print("Extração concluída.\n")

# -------------------------
# 2. Transformação
# -------------------------
print("Transformando dados e calculando métricas...")
metrics = transform(produtos, clientes, vendas)
print("Transformação concluída.\n")

# -------------------------
# 3. Load
# -------------------------
print("Salvando dados em CSV...")
load(metrics)
print("ETL finalizado com sucesso!\n")

# -------------------------
# 4. Forecast (opcional)
# -------------------------
try:
    from forecast import run_forecast
    print("Iniciando forecast (não salvar CSV final)...")
    df_forecast = run_forecast(metrics['receita_diaria'], dias_previsao=30)
    print("Forecast gerado (em memória).\n")
except ImportError:
    print("forecast.py não encontrado, pulando previsão.\n")
