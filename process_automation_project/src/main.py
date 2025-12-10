import pandas as pd
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent

emails = pd.read_excel(ROOT_PATH / r"assets/Emails.xlsx")
vendas = pd.read_excel(ROOT_PATH / r"assets/Vendas.xlsx")
lojas = pd.read_csv(ROOT_PATH / r"assets/Lojas.csv", encoding="latin1", sep=";") 

vendas = vendas.merge(lojas, on="ID Loja")

dicionario_lojas = {}

for loja in lojas["Loja"]:
    dicionario_lojas[loja] = vendas.loc[vendas["Loja"]==loja, :]

data_indicador = vendas["Data"].max()

folder_path = ROOT_PATH / r"database"
arquivos = folder_path.iterdir()
arquivos_backup = [arquivo.name for arquivo in arquivos]

for loja in dicionario_lojas:
    if loja not in arquivos_backup:
         new_folder = folder_path/loja
         new_folder.mkdir()
    
    file = f"{folder_path}/{loja}/{data_indicador.month}_{data_indicador.day}_{loja}.xlsx"
    dicionario_lojas[loja].to_excel(file)

for loja in dicionario_lojas:   
    vendas_loja = dicionario_lojas[loja]
    vendas_dia = vendas_loja.loc[vendas_loja["Data"]==data_indicador, :]
    faturamento_anual = vendas_loja["Valor Final"].sum()
    faturamento_dia = vendas_dia["Valor Final"].sum()
    produtos_ano = len(vendas_loja["Produto"].unique())
    produtos_dia = len(vendas_dia["Produto"].unique())
    print(f"Faturamento da {loja}: Ano: {faturamento_anual} | Dia: {faturamento_dia}")
    print(f"Produtos da {loja}: Ano: {produtos_ano} | Dia: {produtos_dia}")