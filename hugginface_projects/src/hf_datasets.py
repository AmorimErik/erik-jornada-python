import pandas as pd
from datasets import load_dataset

#  Datasets do Hugginface, possibilita baixar a base de dados para sua máquina, o que exige que você tenha espaço em disco e um hardware mais forte para poder rodar localmente as LLMs.

# Carregando um dataset
ds = load_dataset("facebook/natural_reasoning", split="train")
print(ds[0]["question"])


# Carregado um arquivo csv para o pandas.
df = pd.read_csv(
    "hf://datasets/Anthropic/EconomicIndex/release_2025_03_27/automation_vs_augmentation_by_task.csv"
)
print(df)
