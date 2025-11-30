import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path


ROOT_PATH = Path(__file__).parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
cliente = OpenAI(api_key=api_key)

arquivo_audio = ROOT_PATH / f"outputs/audio_criado.mp3"

resposta = cliente.chat.completions.create(
    model="gpt-4o-audio-preview-2025-06-03",
    modalities=["text", "audio"],
    audio={"format": "mp3", "voice": "alloy"},
    messages=[
        {
            "role": "user",
            "content": "Crie um audio para promover meu Git Hub 'Erik Amorim', com foco em desenvolvimento Python e análise de dados.",
        }
    ],
)

audio = base64.b64decode(resposta.choices[0].message.audio.data)

with open(ROOT_PATH / f"outputs/audio_criado.mp3", "wb") as arquivo:
    arquivo.write(audio)
