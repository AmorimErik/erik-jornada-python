import pandas as pd
import openpyxl
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent

caminho = ROOT_PATH / r"assets/Vendas - Dez.xlsx"

tabela = pd.read_excel(caminho)
faturamento = tabela["Valor Final"].sum()
qtde_produtos = tabela["Quantidade"].sum()
print(f"Total de Produtos: {qtde_produtos:,}, Faturamento: {faturamento:,.2f}")
