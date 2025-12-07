import streamlit as st
from langchain_core.messages import HumanMessage
from modelo_openai import memoria, conversas


def abrir_chat(prompt, memoria, conversas):
    # Substituindo a session state pelo gerenciamento de memória do LangChain
    area = st.selectbox(
        "Selecione qual área do Python quer tirar dúvida?",
        options=["Dados", "Sites", "Automção"],
    )
    configuracoes = {"configurable": {"session_id": area}}
    if prompt:
        memoria.invoke({"mensagem": prompt}, config=configuracoes)

    if area in conversas:
        for mensagem in conversas[area].messages:
            if mensagem.type != "system":
                with st.chat_message(mensagem.type):
                    st.write(mensagem.content)


def meu_app():
    st.header("Erik e Python", divider=True)
    st.markdown("#### Tire suas dúvidas sobre Python")
    prompt = st.chat_input("Digite aqui sua dúvida:")
    abrir_chat(prompt, memoria, conversas)


if __name__ == "__main__":
    meu_app()
