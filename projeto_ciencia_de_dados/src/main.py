# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split

# %%
ROOT_PATH = Path(__file__).parent.parent
caminho = ROOT_PATH / "assets"

# %%

meses = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12,
}


# %%
base_airbnb = (
    []
)  # Cria uma lista com bases para união e tratativa posterior, o Pandas não aceita o método append

for arquivo in caminho.iterdir():
    df = pd.read_csv(caminho / arquivo.name)
    df["ano"] = arquivo.name[-8:-4]
    df["mes"] = meses[arquivo.name[:3]]

    base_airbnb.append(df)

base_airbnb = pd.concat(base_airbnb, ignore_index=True)
print(base_airbnb)


# %%
colunas = [
    "host_response_time",
    "host_response_rate",
    "host_is_superhost",
    "host_listings_count",
    "latitude",
    "longitude",
    "property_type",
    "room_type",
    "accommodates",
    "bathrooms",
    "bedrooms",
    "beds",
    "bed_type",
    "amenities",
    "price",
    "security_deposit",
    "cleaning_fee",
    "guests_included",
    "extra_people",
    "minimum_nights",
    "maximum_nights",
    "number_of_reviews",
    "review_scores_rating",
    "review_scores_accuracy",
    "review_scores_cleanliness",
    "review_scores_checkin",
    "review_scores_communication",
    "review_scores_location",
    "review_scores_value",
    "instant_bookable",
    "is_business_travel_ready",
    "cancellation_policy",
    "ano",
    "mes",
]

# %%
base_airbnb = base_airbnb.loc[:, colunas]
print(list(base_airbnb.columns))

# %%%
for coluna in base_airbnb:
    if base_airbnb[coluna].isnull().sum() > 300000:
        base_airbnb = base_airbnb.drop(coluna, axis=1)

print(base_airbnb.isnull().sum())

# %%
base_airbnb = base_airbnb.dropna()

print(base_airbnb.shape)
print(base_airbnb.isnull().sum())

# %%
print(base_airbnb.dtypes)
print("-" * 60)
print(base_airbnb.iloc[0])

# %%
base_airbnb["price"] = base_airbnb["price"].str.replace("$", "")
base_airbnb["price"] = base_airbnb["price"].str.replace(",", "")
base_airbnb["price"] = base_airbnb["price"].astype(np.float32, copy=False)

base_airbnb["extra_people"] = base_airbnb["extra_people"].str.replace("$", "")
base_airbnb["extra_people"] = base_airbnb["extra_people"].str.replace(",", "")
base_airbnb["extra_people"] = base_airbnb["extra_people"].astype(np.float32, copy=False)

base_airbnb["ano"] = base_airbnb["ano"].astype(np.int64, copy=False)

print(base_airbnb.dtypes)
print(base_airbnb["price"].dtypes)

# %%
plt.figure(figsize=(15, 5))
sns.heatmap(base_airbnb.corr(numeric_only=True), annot=True, cmap="Greens")

plt.show()


# %%
def limites(coluna):
    q1 = coluna.quantile(0.25)
    q3 = coluna.quantile(0.75)
    amplitude = q3 - q1
    return q1 - 1.5 * amplitude, q3 + 1.5 * amplitude


def excluir_outliers(df, coluna):
    qtde_linhas = df.shape[0]
    lim_inf, lim_sup = limites(df[coluna])
    df = df.loc[(df[coluna] >= lim_inf) & (df[coluna] <= lim_sup), :]
    linhas_removidas = qtde_linhas - df.shape[0]
    return df, linhas_removidas


def diagrama_caixa(coluna):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(15, 7)
    sns.boxplot(x=coluna, ax=ax1)
    ax2.set_xlim(limites(coluna))
    sns.boxplot(x=coluna, ax=ax2)
    return plt.show()


def histograma(coluna):
    plt.figure(figsize=(15, 7))
    sns.displot(coluna)
    return plt.show()


def grafico_barras(coluna):
    plt.figure(figsize=(15, 7))
    ax = sns.barplot(x=coluna.value_counts().index, y=coluna.value_counts())
    ax.set_xlim(limites(coluna))


# %%
# Preço
diagrama_caixa(base_airbnb["price"])
histograma(base_airbnb["price"])

# %%
base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, "price")
print(f"{linhas_removidas} linhas removidas")

# %%
histograma(base_airbnb["price"])
print(base_airbnb.shape)

# %%
# Pessoa extra
diagrama_caixa(base_airbnb["extra_people"])
histograma(base_airbnb["extra_people"])

# %%
base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, "extra_people")
print(f"{linhas_removidas} linhas reomovidas")

# %%
histograma(base_airbnb["extra_people"])
print(base_airbnb.shape)

# %%
# host_listings_count
diagrama_caixa(base_airbnb["host_listings_count"])
grafico_barras(base_airbnb["host_listings_count"])

# %%
base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, "host_listings_count")
print(f"{linhas_removidas} linhas removidas")

# %%
# Acomodações
diagrama_caixa(base_airbnb["accommodates"])
grafico_barras(base_airbnb["accommodates"])

# %%
base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, "accommodates")
print(f"{linhas_removidas} linhas removidas")

# %%
# Banheiros
diagrama_caixa(base_airbnb["bathrooms"])
plt.figure(figsize=(15, 5))
sns.barplot(
    x=base_airbnb["bathrooms"].value_counts().index,
    y=base_airbnb["bathrooms"].value_counts(),
)

# %%
base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, "bathrooms")
print(f"{linhas_removidas} linhas removidas")

# %%
# Quartos
diagrama_caixa(base_airbnb["bedrooms"])
grafico_barras(base_airbnb["bedrooms"])

# %%
base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, "bedrooms")
print(f"{linhas_removidas} linhas removidas")

# %%
# Camas
diagrama_caixa(base_airbnb["beds"])
grafico_barras(base_airbnb["beds"])

# %%
base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, "beds")
print(f"{linhas_removidas} linhas removidas")

# %%
# Guests Includs
# diagrama_caixa(base_airbnb['guests_included'])
# grafico_barra(base_airbnb['guests_included'])
print(limites(base_airbnb["guests_included"]))
plt.figure(figsize=(15, 5))
sns.barplot(
    x=base_airbnb["guests_included"].value_counts().index,
    y=base_airbnb["guests_included"].value_counts(),
)

# %%
base_airbnb = base_airbnb.drop("guests_included", axis=1)
base_airbnb.shape

# %%
# Noites minimas
diagrama_caixa(base_airbnb["minimum_nights"])
grafico_barras(base_airbnb["minimum_nights"])

# %%
base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, "minimum_nights")
print(f"{linhas_removidas} linhas removidas")

# %%
# Noites máximas
diagrama_caixa(base_airbnb["maximum_nights"])
grafico_barras(base_airbnb["maximum_nights"])

# %%
base_airbnb = base_airbnb.drop("maximum_nights", axis=1)
base_airbnb.shape

# %%
# Número de reviews
diagrama_caixa(base_airbnb["number_of_reviews"])
grafico_barras(base_airbnb["number_of_reviews"])

# %%
base_airbnb = base_airbnb.drop("number_of_reviews", axis=1)
base_airbnb.shape

# %%
# Tipos de propriedades
print(base_airbnb["property_type"].value_counts())

plt.figure(figsize=(15, 5))
grafico = sns.countplot(data=base_airbnb, x="property_type")
grafico.tick_params(axis="x", rotation=90)

# %%
tabela_tipos_casa = base_airbnb["property_type"].value_counts()
colunas_agrupar = []

for tipo in tabela_tipos_casa.index:
    if tabela_tipos_casa[tipo] < 2000:
        colunas_agrupar.append(tipo)
print(colunas_agrupar)

for tipo in colunas_agrupar:
    base_airbnb.loc[base_airbnb["property_type"] == tipo, "property_type"] = "Outros"

print(base_airbnb["property_type"].value_counts())
plt.figure(figsize=(15, 5))
grafico = sns.countplot(data=base_airbnb, x="property_type")
grafico.tick_params(axis="x", rotation=90)

# %%
# Tipos de quartos
print(base_airbnb["room_type"].value_counts())

plt.figure(figsize=(15, 5))
grafico = sns.countplot(data=base_airbnb, x="room_type")
grafico.tick_params(axis="x", rotation=90)

# %%
# bed type
print(base_airbnb["bed_type"].value_counts())

plt.figure(figsize=(15, 5))
grafico = sns.countplot(data=base_airbnb, x="bed_type")
grafico.tick_params(axis="x", rotation=90)

# agrupando categorias de bed_type
tabela_bed = base_airbnb["bed_type"].value_counts()
colunas_agrupar = []

for tipo in tabela_bed.index:
    if tabela_bed[tipo] < 10000:
        colunas_agrupar.append(tipo)
print(colunas_agrupar)

for tipo in colunas_agrupar:
    base_airbnb.loc[base_airbnb["bed_type"] == tipo, "bed_type"] = "Outros"

print(base_airbnb["bed_type"].value_counts())
plt.figure(figsize=(15, 5))
grafico = sns.countplot(data=base_airbnb, x="bed_type")
grafico.tick_params(axis="x", rotation=90)


# %%
# Politica de cancelamento
print(base_airbnb["cancellation_policy"].value_counts())

plt.figure(figsize=(15, 5))
grafico = sns.countplot(data=base_airbnb, x="cancellation_policy")
grafico.tick_params(axis="x", rotation=90)

# agrupando categorias de cancellation_pollicy
tabela_cancellation = base_airbnb["cancellation_policy"].value_counts()
colunas_agrupar = []

for tipo in tabela_cancellation.index:
    if tabela_cancellation[tipo] < 10000:
        colunas_agrupar.append(tipo)
print(colunas_agrupar)

for tipo in colunas_agrupar:
    base_airbnb.loc[
        base_airbnb["cancellation_policy"] == tipo, "cancellation_policy"
    ] = "strict"

print(base_airbnb["cancellation_policy"].value_counts())
plt.figure(figsize=(15, 5))
grafico = sns.countplot(data=base_airbnb, x="cancellation_policy")
grafico.tick_params(axis="x", rotation=90)

# %%
# Amenities
print(base_airbnb["amenities"].iloc[1].split(","))
print(len(base_airbnb["amenities"].iloc[1].split(",")))

base_airbnb["n_amenities"] = base_airbnb["amenities"].str.split(",").apply(len)

# %%
base_airbnb = base_airbnb.drop("amenities", axis=1)
base_airbnb.shape

# %%
diagrama_caixa(base_airbnb["n_amenities"])
grafico_barras(base_airbnb["n_amenities"])

# %%
base_airbnb, linhas_removidas = excluir_outliers(base_airbnb, "n_amenities")
print(f"{linhas_removidas} linhas removidas")

# %%
# Visualização de Mapa das Propriedades
amostra = base_airbnb.sample(n=50000)
centro_mapa = {"lat": amostra.latitude.mean(), "lon": amostra.longitude.mean()}
mapa = px.density_mapbox(
    amostra,
    lat="latitude",
    lon="longitude",
    z="price",
    radius=2.5,
    center=centro_mapa,
    zoom=10,
    mapbox_style="open-street-map",
)

mapa.show()
# %%
print(base_airbnb.columns)
# %%
colunas_tf = ["host_is_superhost", "instant_bookable", "is_business_travel_ready"]
base_airbnb_cod = base_airbnb.copy()

for coluna in colunas_tf:
    base_airbnb_cod.loc[base_airbnb_cod[coluna] == "t", coluna] = 1
    base_airbnb_cod.loc[base_airbnb_cod[coluna] == "f", coluna] = 0

colunas_categoria = [
    "property_type",
    "room_type",
    "bed_type",
    "bed_type",
    "cancellation_policy",
]
base_airbnb_cod = pd.get_dummies(data=base_airbnb_cod, columns=colunas_categoria)
print(base_airbnb_cod.head())


# %%
def avaliar_modelo(nome_modelo, y_teste, previsao):
    r2 = r2_score(y_teste, previsao)
    RSME = np.sqrt(mean_squared_error(y_teste, previsao))
    return f"Modelo {nome_modelo}:\nR²: {r2}\nRSME: {RSME}"


# %%
modelo_rf = RandomForestRegressor()
modelo_lr = LinearRegression()
# modelo_et = ExtraTreesRegressor(n_estimators=100, n_jobs=1, max_depth=15, random_state=10)
modelo_et = ExtraTreesRegressor()
modelos = {
    "RandomForest": modelo_rf,
    "LinearRegression": modelo_lr,
    "EtraTrees": modelo_et,
}

y = base_airbnb_cod["price"]
x = base_airbnb_cod.drop("price", axis=1)

#%%
# 1. Verificar tamanho dos dados antes de começar
memoria_estimada = (
    x.memory_usage(deep=True).sum() / (1024**2)
    if hasattr(x, "memory_usage")
    else "Desconhecido"
)
print(f"Iniciando treinamento. Shape: {x.shape}. Tamanho aprox: {memoria_estimada} MB")

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=10)

for nome_modelo, modelo in modelos.items():
    print(f"--> Iniciando treinamento de: {nome_modelo}...")

    try:
        # Treinando o modelo
        modelo.fit(x_train, y_train)
        print(f"    (Fit concluído para {nome_modelo})")

        # Testando o modelo
        previsao = modelo.predict(x_test)
        print(avaliar_modelo(nome_modelo, y_test, previsao))
        print("-" * 30)

    except Exception as e:
        print(f"ERRO ao treinar {nome_modelo}: {e}")

# %%
