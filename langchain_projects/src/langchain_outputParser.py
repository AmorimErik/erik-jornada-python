from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_PATH = Path(__file__).parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
modelo = OpenAI(api_key=api_key)

parser = CommaSeparatedListOutputParser()
forma = PromptTemplate.from_template(
    "Formato da resposta: {formato}",
    partial_variables={"formato": parser.get_format_instructions()},
)
idioma = PromptTemplate.from_template(
    "Os textos da sua resposta devem estar em {idioma}",
    partial_variables={"idioma": "portugues"},
)
mensagem = PromptTemplate.from_template("Mensagem do usuário: {mensagem}")
template = forma + idioma + mensagem

msg_usuario = input("Faça sua solicitação: ")
prompt = template.invoke({"mensagem": msg_usuario})
resposta = parser.invoke(modelo.invoke(prompt))

print(resposta)
