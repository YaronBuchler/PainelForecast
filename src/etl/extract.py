import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../db'))
import pandas as pd
from connection import get_connection

def extract():
    conn = get_connection()
    df_produtos = pd.read_sql_query("SELECT * FROM produtos", conn)
    df_clientes = pd.read_sql_query("SELECT * FROM clientes", conn)
    df_vendas = pd.read_sql_query("SELECT * FROM vendas", conn)
    conn.close()
    return df_produtos, df_clientes, df_vendas

if __name__ == "__main__":
    produtos, clientes, vendas = extract()
    print("Extração concluída")
