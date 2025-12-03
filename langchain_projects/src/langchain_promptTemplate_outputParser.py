from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_PATH = Path(__file__).parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
modelo = ChatOpenAI(api_key=api_key)

chat = ChatPromptTemplate(
    [
        SystemMessage(
            "Responda o usuário sempre em {idioma} independente da lingua que ele utilize na pergunta."
        )
    ],
    partial_variables={"idioma": "portugues"},
)

msg_usuario = HumanMessage(input("Digite sua solicitação: "))
chat.append(msg_usuario)
prompt = chat.invoke({})
parser = StrOutputParser()
resposta = parser.invoke((modelo.invoke(prompt)))
print(resposta)
