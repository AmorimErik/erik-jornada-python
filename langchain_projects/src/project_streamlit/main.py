import streamlit as st
from langchain_core.messages import HumanMessage
from modelo_openai import chain


def abrir_chat(prompt, chain):
    if "messagens" in st.session_state:
        mensagens = st.session_state["mensagens"]
    else:
        mensagens = []
        st.session_state["mensagens"] = mensagens

    if prompt:
        mensagens = [HumanMessage(prompt)]
        resposta = chain.invoke({"history": mensagens})
        mensagens.append(resposta)
        for mensagem in mensagens:
            if mensagem.type != "system":
                with st.chat_message(mensagem.type):
                    st.write(mensagem.content)


def meu_app():
    st.header("Erik e Python", divider=True)
    st.markdown("#### Tire suas dúvidas sobre Python")
    prompt = st.chat_input("Digite aqui sua dúvida:")
    abrir_chat(prompt, chain)


if __name__ == "__main__":
    meu_app()
