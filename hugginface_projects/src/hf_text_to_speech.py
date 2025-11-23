from transformers import VitsModel, AutoTokenizer
import soundfile as sf
import torch
import os

modelo = VitsModel.from_pretrained("facebook/mms-tts-por")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-por")

prompt = "Python é a melhor linguagem de programação. Se você discorda, está errado."

inputs = tokenizer(prompt, return_tensors="pt")

with torch.no_grad():
    output = modelo(**inputs)


audio = output.waveform[0].numpy()
sampling_rate = modelo.config.sampling_rate

caminho = r"hugginface_projects/arquivos_salvos"
arquivo = "speech.wav"
os.makedirs(caminho, exist_ok=True)

sf.write(f"{caminho}/{arquivo}", audio, samplerate=sampling_rate)

print("Arquivo gerado com sucesso!")
