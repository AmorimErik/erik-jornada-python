import pandas as pd
import undetected_chromedriver as uc  # Essa biblioteca faz com quê o Google não reconheça o robô.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent

options = uc.ChromeOptions()
nav = uc.Chrome(options=options)

tabela_produtos = pd.read_excel("assets/buscas.xlsx")

nav.get("https://google.com")

produto = "Iphone 12 64GB"
nav.find_element("xpath", "//*[@id='APjFqb']").send_keys(produto, Keys.ENTER)
elemento = nav.find_element(
    By.PARTIAL_LINK_TEXT, "Shopping"
)  # Como a classe muda sempre, consegui pegar utilizando parte do nome do link.
elemento.click()


try:
    input("Pressione Enter no terminal para fechar o navegador...")
finally:
    nav.quit()
