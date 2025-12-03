import streamlit as st
from langchain_modelo_openai import modelo, mensagens
from langchain_core.messages import HumanMessage, SystemMessage

def abrir_chat(prompt, modelo, mensagens):
    if "mensagens" in st.session_state:
        mensagens = st.session_state["mensagens"]
    else:
        st.session_state["mensagens"] = mensagens
    
    if prompt:
        mensagens.append(HumanMessage(prompt))
        resposta = modelo.invoke(mensagens)
        mensagens.append(resposta)
        
    for mensagem in mensagens:
        if not isinstance(mensagem, SystemMessage):
            with st.chat_message(mensagem.type):
                st.write(mensagem.content)


def meu_app():
    st.header("ErikGPT", divider=True)
    st.markdown("#### Converse com o ChatGPT integrado no Streamlit.")
    prompt = st.chat_input("Digite sua mensagem:")
    abrir_chat(prompt, modelo, mensagens)
    
meu_app()