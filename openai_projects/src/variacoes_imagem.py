import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path


ROOT_PATH = Path(__file__).parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
cliente = OpenAI(api_key=api_key)

with open(ROOT_PATH / "assets/imagem.jpg", "rb") as arquivo_imagem:
    resposta = cliente.images.create_variation(
        model="dall-e-2", n=3, image=arquivo_imagem
    )

imagens = resposta.data

for i, imagem in enumerate(imagens, start=1):
    url_imagem = imagem.url
    informacoes_imagem = requests.get(url_imagem)
    with open(ROOT_PATH / f"outputs/variacao{i}.jpg", "wb") as arquivo_imagem:
        arquivo_imagem.write(informacoes_imagem.content)
