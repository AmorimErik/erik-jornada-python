import streamlit as st
from hf_api_inference_client import resumir
from hf_api_inference_text_generation import criar_texto
from hf_api_chatcompletion import chat


def gerar_texto(prompt):
    st.markdown("##### Informe o tema que deseja que o texto seja gerado.")
    if prompt:
        resposta = criar_texto(prompt)
        st.write(resposta)


def resumir_texto(prompt):
    st.markdown("##### Insira o texto que deseja resumir na caixa de prompt.")
    if prompt:
        resposta = resumir(prompt)
        st.write(resposta)


def abrir_chat(prompt):
    st.markdown("##### Converse com a IA do Erik-IAs.")
    if "mensagens" not in st.session_state:
        mensagens = [
            {
                "role": "system",
                "content": "Responda as perguntas de forma correta e precisa.",
            }
        ]
        st.session_state["mensagens"] = mensagens
    else:
        mensagens = st.session_state["mensagens"]

    if prompt:
        msg_usuario = {"role": "user", "content": prompt}
        mensagens.append(msg_usuario)
        mensagens = chat(mensagens)

        for mensagem in mensagens:
            role = mensagem["role"]
            content = mensagem["content"]
            if role != "system":
                with st.chat_message(role):
                    st.write(content)


def main_app():
    # titulo
    st.header("Erik-IAs", divider=True)
    # subtitulo
    st.markdown("#### Selecione a IA que mais te ajuda.")
    # selectbox
    opcoes = ["Gerar Texto", "Resumir Texto", "Abrir Chat"]
    opcao_selecionada = st.selectbox("Selecione uma opção de IA.", options=opcoes)
    # prompt
    prompt = st.chat_input("Digite aqui: ")

    if opcao_selecionada:
        if opcao_selecionada == opcoes[0]:
            gerar_texto(prompt)
        elif opcao_selecionada == opcoes[1]:
            resumir_texto(prompt)
        else:
            abrir_chat(prompt)


main_app()
