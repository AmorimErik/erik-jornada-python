# Cria um chat com o usuário, perguntas e respostas.

from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "env", ".env")

load_dotenv(dotenv_path)


def chat(mensagens):
    cliente = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct")
    resposta = cliente.chat_completion(mensagens)
    resposta_ia = resposta.choices[0]
    resposta_role = resposta_ia.message.role
    resposta_content = resposta_ia.message.content
    dic_resposta_ia = {"role": resposta_role, "content": resposta_content}
    mensagens.append(dic_resposta_ia)
    return mensagens


mensagens = [
    {"role": "system", "content": "Responda as perguntas de forma correta e precisa."}
]

print(f"Resposta: {chat(mensagens)}")
