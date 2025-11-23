# Cria uma imagem a partir de um enunciado.

from diffusers import StableDiffusionPipeline
import os

model_id = "sd-legacy/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to("cpu")

prompt = "the photo of Bugs Bunny playing the guitar and admiring the mountain."
image = pipe(prompt).images[0]

caminho = r"hugginface_projects/arquivos_salvos"
arquivo = "pernalonga.png"
os.makedirs(caminho, exist_ok=True)

image.save(f"{caminho}/{arquivo}")
print("Imagem gerada com sucesso!")
