# Gera um texto a partir de uma solicitação.
from transformers import pipeline

pipe = pipeline(
    "text-generation", model="ahxt/llama2_xs_460M_experimental", device="cpu"
)

prompt = "What is Python Programming Language?"
resposta = pipe(prompt)

print(f"Resposta: \n{resposta}")
