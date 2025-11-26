# Este código extrai um áudio do vídeo e o transcreve para um arquivo "srt"

import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from pydub import AudioSegment

ROOT_PATH = Path(__file__).parent.parent  # sobe dois níveis até a pasta raiz.

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
cliente = OpenAI(api_key=api_key)

arquivo_video = ROOT_PATH / "assets/ja começou a jornada full stack.mp4"
arquivo_srt = ROOT_PATH / "outputs/transcricao_video.srt"


audio = AudioSegment.from_file(file=arquivo_video, format="mp4")
audio.export(ROOT_PATH / "outputs/audio_video.mp3", format="mp3")

try:
    with open(ROOT_PATH / "outputs/audio_video.mp3", "rb") as arquivo_saida:
        transcricao = cliente.audio.transcriptions.create(
            file=arquivo_saida, model="whisper-1", language="pt", response_format="srt"
        )

    with open(arquivo_srt, "w", encoding="utf-8") as arquivo_legenda:
        arquivo_legenda.write(transcricao)

except FileNotFoundError:
    print(f"❌ Erro: O arquivo de áudio não foi encontrado em: {arquivo_video}")
