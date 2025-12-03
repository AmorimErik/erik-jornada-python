from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_PATH = Path(__file__).parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
modelo = OpenAI(api_key=api_key)

# Formato unificado de configuração do template de como a AI deve responder ao usuário.
template_prompt = PromptTemplate.from_template(
    "Responda ao usuário em no máximo {tamanho} caracteres, responda em {idioma}, independente da lingua que o usuário fizer a pergunta. Pergunta do usuário: {mensagem}",
    partial_variables={"tamanho": 150, "idioma": "portugues"},
)

# Segmentação das variaveis que compoem o template de configuração da AI.
formato = PromptTemplate.from_template(
    "Responda o usuário de forma educada e informal, como se fosse um amigo próximo."
)
tamanho = PromptTemplate.from_template(
    "Sua resposta de conter no máximo {tamanho} caracteres.",
    partial_variables={"tamanho": 150},
)
idioma = PromptTemplate.from_template(
    "Responda em {idioma}, independente da lingua utilizada pelo usuário.",
    partial_variables={"idioma": "portugues"},
)
mensagem = PromptTemplate.from_template("Mensagem do usuário: {msg_usuario}")
template = formato + tamanho + idioma + mensagem

msg_usuario = input("Digite uma pergunta: ")
prompt = template_prompt.invoke({"mensagem": msg_usuario})

resposta = modelo.invoke(prompt)
print(resposta)
