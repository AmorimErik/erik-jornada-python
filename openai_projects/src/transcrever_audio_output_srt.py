# Este código gera um arquivo de saida em srt, onde consta o tempo de cada transcrição dentro do áudio.

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
arquivo_saida = ROOT_PATH / "outputs/transcricao.srt"

try:
    resposta = cliente.audio.transcriptions.create(
        model="whisper-1", file=arquivo_entrada, response_format="srt"
    )

    with open(arquivo_saida, "w", encoding="utf-8") as arquivo_saida:
        arquivo_saida.write(resposta)

except FileNotFoundError:
    print(f"❌ Erro: O arquivo de áudio não foi encontrado em: {arquivo_entrada}")
