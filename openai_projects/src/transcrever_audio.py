import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent  # sobe dois níveis até a pasta raiz.

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
cliente = OpenAI(api_key=api_key)

arquivo_entrada = ROOT_PATH / "assets/audio.mp3"
arquivo_saida = ROOT_PATH / "outputs/transcricao.txt"

try:
    with open(arquivo_entrada, "rb") as arquivo_audio:
        transcricao = cliente.audio.transcriptions.create(
            model="gpt-4o-transcribe", file=arquivo_audio
        )

except FileNotFoundError:
    print(f"❌ Erro: O arquivo de áudio não foi encontrado em: {arquivo_entrada}")

arquivo_saida.write_text(transcricao.text, encoding="utf-8")
