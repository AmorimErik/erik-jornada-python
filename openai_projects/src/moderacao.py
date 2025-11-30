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

resposta = cliente.moderations.create(
    model="omni-moderation-2024-09-26",
    input={"TEXTO_TESTE"},
)

print(resposta.results[0].flagged)
print(resposta.results[0].categories.to_dict())
