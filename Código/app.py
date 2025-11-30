# app.py
import streamlit as st
from frontend import FrontEnd  # Importa sua classe FrontEnd

# Define a configuração básica da página
st.set_page_config(
    page_title="Sistema de Gerenciamento de Livros",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Cria uma instância da classe FrontEnd e roda a função principal
if __name__ == "__main__":
    # Remove o título padrão que aparece no topo e que está sendo controlado na função renderizar_listar
    st.title("Sistema de Gerenciamento de Livros")
    app = FrontEnd()
    app.rodar()
