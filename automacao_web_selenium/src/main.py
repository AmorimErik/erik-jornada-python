import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent

nav = webdriver.Chrome()

tabela_produtos = pd.read_excel("assets/buscas.xlsx")

nav.get("https://google.com")

produto = "Iphone 12 64GB"
nav.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div/div[2]/input').send_keys(produto, Keys.ENTER)
