from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_PATH = Path(__file__).parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
modelo = ChatOpenAI(api_key=api_key)

mensagens = [SystemMessage("Responda as perguntas de forma curta, com no máximo 150 caracteres")]

if __name__ == "__main__":
    mensagem_usuario = input("Digite sua mensagem: ")

    mensagens.append(HumanMessage(mensagem_usuario))

    resposta = modelo.invoke(mensagens)
    print(f"Resposta: {resposta}\n")
    print(f"Tipo: {type(resposta)}\n")
    print(f"Conteúdo da resposta: {resposta.content}\n")
    print(f"Origem da resposta: {resposta.type}\n")
