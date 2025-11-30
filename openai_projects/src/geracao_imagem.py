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

resposta = cliente.images.generate(
    model="gpt-image-1-mini",
    prompt="Uma imagem do pernalonga tocando berimbau e apreciando o vale do alto da montanha",
    size="1024x1024",
)

imagem = requests.get(resposta.data[0].url)

with open(ROOT_PATH / "outputs/imagem.png", "wb") as arquivo:
    arquivo.write(imagem.content)
