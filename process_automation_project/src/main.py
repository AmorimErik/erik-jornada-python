import pandas as pd
from pathlib import Path
from enviar_email import enviar_email

ROOT_PATH = Path(__file__).parent.parent

# Metas a serem atingidas.
meta_faturamento_dia = 1000
meta_faturamento_ano = 1650000
meta_qtde_produtos_dia = 4
meta_qtde_produtos_ano = 120
meta_ticket_medio_dia = 500
meta_ticket_medio_ano = 500


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
    valor_venda = vendas_loja.groupby("Código Venda").sum(numeric_only=True)
    ticket_medio_ano = valor_venda["Valor Final"].mean()
    valor_venda_dia = vendas_dia.groupby("Código Venda").sum(numeric_only=True)
    ticket_medio_dia = valor_venda_dia["Valor Final"].mean()

    destinatario_email = emails.loc[emails["Loja"] == loja, "E-mail"].iloc[0]
    assunto_email = (
        f"OnePage Dia {data_indicador.day}/{data_indicador.month} - Loja {loja}"
    )

    if faturamento_dia >= meta_faturamento_dia:
        cor_fat_dia = "green"
    else:
        cor_fat_dia = "red"
    if faturamento_anual >= meta_faturamento_ano:
        cor_fat_ano = "green"
    else:
        cor_fat_ano = "red"
    if produtos_dia >= meta_qtde_produtos_dia:
        cor_qtde_dia = "green"
    else:
        cor_qtde_dia = "red"
    if produtos_ano >= meta_qtde_produtos_ano:
        cor_qtde_ano = "green"
    else:
        cor_qtde_ano = "red"
    if ticket_medio_dia >= meta_ticket_medio_dia:
        cor_ticket_dia = "green"
    else:
        cor_ticket_dia = "red"
    if ticket_medio_ano >= meta_ticket_medio_ano:
        cor_ticket_ano = "green"
    else:
        cor_ticket_ano = "red"

    corpo_email = f"""
    <p>Bom dia, {destinatario_email}</p>

    <p>O resultado de ontem <strong>({data_indicador.day}/{data_indicador.month})</strong> da <strong>Loja {loja}</strong> foi:</p>

    Tabela
    <table>
    <tr>
        <th>Indicador</th>
        <th>Valor dia</th>
        <th>Meta dia</th>
        <th>Cenário dia</th>
    </tr>
    <tr>
        <td>Faturamento</td>
        <td style="text-align: center">{faturamento_dia:.2f}</td>
        <td style="text-align: center">{meta_faturamento_dia:.2f}</td>
        <td style="text-align: center"><font color="{cor_fat_dia}">◙</font></td>
    </tr>
    <tr>
        <td>Diversidade de Produtos</td>
        <td style="text-align: center">{produtos_dia:.2f}/<td>
        <td style="text-align: center">{meta_qtde_produtos_dia:.2f}</td>
        <td style="text-align: center"><font color="{cor_qtde_dia}">◙</font></td>
    </tr>
    <tr>
        <td>Ticket Médio</td>
        <td style="text-align: center">{ticket_medio_dia:.2f}</td>
        <td style="text-align: center">{meta_ticket_medio_dia:.2f}</td>
        <td style="text-align: center"><font color="{cor_ticket_dia}">◙</font></td>
    </tr>
    </table>
    <br>
    <table>
    <tr>
        <th>Indicador</th>
        <th>Valor Ano</th>
        <th>Meta dia</th>
        <th>Cenário dia</th>
    </tr>
    <tr>
        <td>Faturamento</td>
        <td style="text-align: center">{faturamento_anual:.2f}</td>
        <td style="text-align: center">{meta_faturamento_ano:.2f}</td>
        <td style="text-align: center"><font color="{cor_fat_ano}">◙</font></td>
    </tr>
    <tr>
        <td>Diversidade de Produtos</td>
        <td style="text-align: center">{produtos_ano:.2f}/<td>
        <td style="text-align: center">{meta_qtde_produtos_ano:.2f}</td>
        <td style="text-align: center"><font color="{cor_qtde_ano}">◙</font></td>
    </tr>
    <tr>
        <td>Ticket Médio</td>
        <td style="text-align: center">{ticket_medio_ano:.2f}</td>
        <td style="text-align: center">{meta_ticket_medio_ano:.2f}</td>
        <td style="text-align: center"><font color="{cor_ticket_ano}">◙</font></td>
    </tr>
    </table>

    <p>Segue em anexo a planilha com todos os dados para mais detalhes.</p>

    <p>Qualquer dúvida estou à disposição.</p>
    <p>Att., Erik</p>
    """

    anexo = (
        f"{folder_path}/{loja}/{data_indicador.month}_{data_indicador.day}_{loja}.xlsx"
    )

    # enviar_email(data_indicador, loja, anexo, destinatario_email, corpo_email)


faturamento_lojas = vendas.groupby("Loja")[["Loja", "Valor Final"]].sum(
    numeric_only=True
)
faturamento_lojas_ano = faturamento_lojas.sort_values(by="Valor Final", ascending=False)

faturamento_lojas_ano.to_excel(
    f"{folder_path}/{data_indicador.day}_{data_indicador.month}_Ranking Anual.xlsx"
)


vendas_dia = vendas.loc[vendas["Data"] == data_indicador, :]
faturamento_lojas_dia = vendas.groupby("Loja")[["Loja", "Valor Final"]].sum(
    numeric_only=True
)
faturamento_lojas_dia = faturamento_lojas_dia.sort_values(
    by="Valor Final", ascending=False
)

faturamento_lojas_dia.to_excel(
    f"{folder_path}/{data_indicador.day}_{data_indicador.month}_Ranking dia.xlsx"
)
