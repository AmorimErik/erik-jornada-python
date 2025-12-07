import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

ROOT_PATH = Path(__file__).parent.parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
modelo = ChatOpenAI(api_key=api_key)

conversas = dict()


def sessao_usuario(session_id):
    if session_id not in conversas:
        conversas[session_id] = InMemoryChatMessageHistory()
    return conversas[session_id]


# Ajustes para que o código funcione corretamente com LangChain.
template = ChatPromptTemplate(
    [
        (
            "system",
            "Responda o usuário com respostas diretas e o mais curtas possíveis, mas sempre respondento a dúvida dele. As dúvidas são referentes a programação em {tema}. Qualquer outra dúvida que não seja desse tema, apenas responda: não sou especialista no tema.",
        ),
        ("placeholder" "{history}"),
        ("user", "{mensagem}"),
    ],
    partial_variables={"tema": "Python"},
)

chain = template | modelo
memoria = RunnableWithMessageHistory(
    chain,
    get_session_history=sessao_usuario,
    input_messages_key="mensagem",
    history_messages_key="history",
)
