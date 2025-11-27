from funcao_extrair_audio import legendar
import streamlit as st


def meu_app():
    st.header("Gerador de legendas de áudio", divider=True)
    st.markdown("#### Gere a legenda de qualquer vídeo ou áudio automaticamente.")

    arquivo = st.file_uploader(
        "Selecione o vídeo [.mp4] ou áudio [.mp3] para legendar", type=["mp3", "mp4"]
    )
    if arquivo:
        legenda = legendar(arquivo)
        st.write(f"Arquivo{arquivo.name} legendado com sucesso")
        st.write(legenda)


if __name__ == "__main__":
    meu_app()
