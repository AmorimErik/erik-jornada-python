import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path


ROOT_PATH = Path(__file__).parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
cliente = OpenAI(api_key=api_key)

arquivo_audio = ROOT_PATH / f"outputs/audio_criado.mp3"

with openai.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="ash",
    input="Aprender Python é importante por ser uma linguagem versátil e popular, utilizada em áreas de ponta como inteligência artificial, machine learning, ciência de dados e automação, além de ser amplamente empregada no desenvolvimento web.",
) as resposta:
    resposta.stream_to_file(arquivo_audio)
