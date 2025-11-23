# Recebe um texto e faz o resumo dele.

from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "env", ".env")

load_dotenv(dotenv_path)


def resumir(texto):
    cliente = InferenceClient()
    resposta = cliente.summarization(
        texto, model="facebook/bart-large-cnn"
    ).summary_text
    return resposta


texto = """
    Greek (Modern Greek: Ελληνικά, romanized: Elliniká,  
    The Greek language holds a very important place in the history of the Western world. Beginning with the epics of Homer, ancient Greek literature includes many works of lasting importance in the European canon. Greek is also the language in which many of the foundational texts in science and philosophy were originally composed. The New Testament of the Christian Bible was also originally written in Greek.[14][15] Together with the Latin texts and traditions of the Roman world, the Greek texts and Greek societies of antiquity constitute the objects of study of the discipline of Classics.

    During antiquity, Greek was by far the most widely spoken lingua franca in the Mediterranean world.[16] It eventually became the official language of the Byzantine Empire and developed into Medieval Greek.[17] In its modern form, Greek is the official language of Greece and Cyprus and one of the 24 official languages of the European Union. It is spoken by at least 13.5 million people today in Greece, Cyprus, Italy, Albania, Turkey, and the many other countries of the Greek diaspora.

    Greek roots have been widely used for centuries and continue to be widely used to coin new words in other languages; Greek and Latin are the predominant sources of international scientific vocabulary."""

print(resumir(texto))
