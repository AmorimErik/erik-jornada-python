import pandas as pd
import undetected_chromedriver as uc  # Essa biblioteca faz com quê o Google não reconheça o robô.
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent

options = uc.ChromeOptions()
nav = uc.Chrome(options=options)

tabela_produtos = pd.read_excel("assets/buscas.xlsx")


def busca_google_shopping(nav, produto, termos_banidos, preco_minimo, preco_maximo):
    nav.get("https://google.com")
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    preco_maximo = float(preco_maximo)
    preco_minimo = float(preco_minimo)
    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_produtos = produto.split(" ")

    nav.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input"
    ).send_keys(produto)
    nav.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input"
    ).send_keys(Keys.ENTER)

    elementos = nav.find_elements(By.CLASS_NAME, "hdtb-mitem")
    for item in elementos:
        if "Shopping" in item.text:
            item.click()
            break

    lista_resultados = nav.find_elements(By.CLASS_NAME, "sh-dgr__grid-result")

    lista_ofertas = []
    for resultado in lista_resultados:
        nome = resultado.find_element(By.CLASS_NAME, "Xjkr3b").text
        nome = nome.lower()
        tem_termos_banidos = False
        for palavra in lista_termos_banidos:
            if palavra in nome:
                tem_termos_banidos = True

        tem_todos_termos_produto = True
        for palavra in lista_termos_produtos:
            if palavra not in nome:
                tem_todos_termos_produto = False

        if not tem_termos_banidos and tem_todos_termos_produto:
            try:
                preco = resultado.find_element(By.CLASS_NAME, "a8Pemb").text
                preco = (
                    preco.replace("R$", "")
                    .replace(" ", "")
                    .replace(".", "")
                    .replace(",", ".")
                )
                preco = float(preco)
                if preco_minimo <= preco <= preco_maximo:
                    elemento_link = resultado.find_element(By.CLASS_NAME, "aULzUe")
                    elemento_pai = elemento_link.find_element(By.XPATH, "..")
                    link = elemento_pai.get_attribute("href")
                    lista_ofertas.append((nome, preco, link))
            except:
                continue

    return lista_ofertas


def busca_buscape(nav, produto, termos_banidos, preco_minimo, preco_maximo):
    preco_maximo = float(preco_maximo)
    preco_minimo = float(preco_minimo)
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_produto = produto.split(" ")

    nav.get("https://www.buscape.com.br/")

    nav.find_element(By.CLASS_NAME, "search-bar__text-box").send_keys(
        produto, Keys.ENTER
    )

    time.sleep(5)
    lista_resultados = nav.find_elements(By.CLASS_NAME, "Cell_Content__1630r")

    lista_ofertas = []
    for resultado in lista_resultados:
        try:
            preco = resultado.find_element(
                By.CLASS_NAME, "CellPrice_MainValue__3s0iP"
            ).text
            nome = resultado.get_attribute("title")
            nome = nome.lower()
            link = resultado.get_attribute("href")

            tem_termos_banidos = False
            for palavra in lista_termos_banidos:
                if palavra in nome:
                    tem_termos_banidos = True

            tem_todos_termos_produto = True
            for palavra in lista_termos_produto:
                if palavra not in nome:
                    tem_todos_termos_produto = False

            if not tem_termos_banidos and tem_todos_termos_produto:
                preco = (
                    preco.replace("R$", "")
                    .replace(" ", "")
                    .replace(".", "")
                    .replace(",", ".")
                )
                preco = float(preco)
                if preco_minimo <= preco <= preco_maximo:
                    lista_ofertas.append((nome, preco, link))
        except:
            pass
    return lista_ofertas


tabela_ofertas = pd.DataFrame()

for linha in tabela_produtos.index:
    produto = tabela_produtos.loc[linha, "Nome"]
    termos_banidos = tabela_produtos.loc[linha, "Termos banidos"]
    preco_minimo = tabela_produtos.loc[linha, "Preço mínimo"]
    preco_maximo = tabela_produtos.loc[linha, "Preço máximo"]

    lista_ofertas_google_shopping = busca_google_shopping(
        nav, produto, termos_banidos, preco_minimo, preco_maximo
    )
    if lista_ofertas_google_shopping:
        tabela_google_shopping = pd.DataFrame(
            lista_ofertas_google_shopping, columns=["produto", "preco", "link"]
        )
        tabela_ofertas = tabela_ofertas.append(tabela_google_shopping)
    else:
        tabela_google_shopping = None

    lista_ofertas_buscape = busca_buscape(
        nav, produto, termos_banidos, preco_minimo, preco_maximo
    )
    if lista_ofertas_buscape:
        tabela_buscape = pd.DataFrame(
            lista_ofertas_buscape, columns=["produto", "preco", "link"]
        )
        tabela_ofertas = tabela_ofertas.append(tabela_buscape)
    else:
        tabela_buscape = None

tabela_ofertas = tabela_ofertas.reset_index(drop=True)
tabela_ofertas.to_excel("Ofertas.xlsx", index=False)
