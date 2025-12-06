from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_PATH = Path(__file__).parent.parent

dotenv_path = ROOT_PATH / "env/.env"
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
modelo = ChatOpenAI(api_key=api_key)


class Avaliacao(BaseModel):
    "Review foi enviado por um cliente que comprou um produto, preciso avaliar esse produto para saber se ele é bom e se vale a pena"

    review_positivo: bool = Field(description="Essa avaliação foi positiva?")
    vale_a_pena: bool = Field(
        description="Essa avaliação no geral diz que vale a pena comprar esse produto?"
    )
    pontos_positivos: list[str] = Field(
        description="Quais os principais pontos positivos dessa avaliação? (cada ponto em no máximo 3 palavras, se houver)"
    )
    pontos_negativos: list[str] = Field(
        description="Quais os principais pontos negativos dessa avaliação? (cada ponto em no máximo 3 palavras, se houver)"
    )


class ListaAvaliacoes(BaseModel):
    avaliacoes: list[Avaliacao] = Field(
        description="Lista com as avaliações de cada review."
    )


parser = JsonOutputParser(name="avaliacao_usuario", pydantic_object=ListaAvaliacoes)
instrucoes = parser.get_format_instructions()
contexto = PromptTemplate.from_template(
    "Você está avaliando reviews de vários usuários sobre um produto, preciso de algumas informações extraídas de cada review dessa lista de reviews: {reviews}"
)
idioma = PromptTemplate.from_template(
    "Responda sempre em {idioma}", partial_variables={"idioma": "portugues"}
)
formato = PromptTemplate.from_template(
    "Formato da resposta: {formato}", partial_variables={"formato": instrucoes}
)
template = contexto + idioma + formato


reviews = [
    "Eu gostei bastante da câmera é a primeira vez que eu tiro foto com câmeras tirei algumas fotos não de pessoas no momento mas de algum objeto vou postar pra vocês verem",
    "Perfect!!! top de linha, vem com tudo que é descrito e ganhei um brinde maravilhoso. Verifiquei tudo, procedência etc etc. Tudo ok, não vão se arrepender!.",
    "Uma das melhores câmeras custo benefício para iniciantes da canon. Boa conectividade. Facilidade de aprender a mexer. Vale a pena pra quem não quer gastar muito mas quer ter câmera semi profissional.",
    "A apresentação da câmera é muito boa, mas preciso de uma câmera menor e mais compacta.",
]

chain = template | modelo | parser

template_analise = PromptTemplate.from_template(
    """
    Analise a seguinte lista de reviews de um produto e me diga:
    1. Quantas reviews são positivas e quantas são negativas (e o percentual de reviews positivas do total);
    2. Qual percentual de reviews diz que vale a pena comprar o produto;
    3. O ponto positivo que mais aparece e o ponto negativo que mais aparece.
    A lista de reviews é essa: {avaliacoes}    
"""
)

parser_texto = StrOutputParser()

chain_analise = template_analise | modelo | parser_texto

chain_global = chain | chain_analise

resposta = chain_global.invoke({"reviews": reviews})

with open(ROOT_PATH / "arquivos/reviews.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{resposta}\n")

print(resposta)
