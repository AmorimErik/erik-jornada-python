from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "env", ".env")

load_dotenv(dotenv_path)


def criar_texto(prompt):
    cliente = InferenceClient()
    resposta = (
        cliente.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct",
            messages=[{"role": "user", "content": prompt}],
        )
        .choices[0]
        .message.content
    )
    return resposta


prompt = "O que é a Linguagem de Programação Python"
print(f"Resposta: \n{criar_texto(prompt)}")
