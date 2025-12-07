import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import MessagesPlaceholder

ROOT_PATH = Path(__file__).parent.parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
modelo = ChatOpenAI(api_key=api_key)

template = ChatPromptTemplate(
    [
        SystemMessage(
            "Responda o usuário com respostas diretas e o mais curtas possíveis, mas sempre respondento a dúvida dele. As dúvidas são referentes a programação em {tema}. Qualquer outra dúvida que não seja desse tema, apenas responda: não sou especialista no tema."
        ),
        MessagesPlaceholder("history"),
    ],
    partial_variables={"tema": "Python"},
)

chain = template | modelo
