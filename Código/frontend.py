#Esse é a part front-end do sistema, pra ficar mais organizado qualquer coisa avisa
#Lembra de fazer o seu venv (o meu ta no gitignore, que não é visto pelo git e github), e baixar o streamlit (pip install streamlit, ja com venv ativado)
import streamlit as st #Fazer o front-end em si, para rodar, vai no terminal e digita "streamlit run {caminho relativo} "
from backend import BackEnd #Importar o backend pra vc conseguir usar e testar aq
class FrontEnd: #Recomendo fazer type hinting e POO pq fica chiquérrimo
    def __init__(self) -> None:
        self.estoque=BackEnd()
        self.produtos=self.estoque.lista_livros
    def renderizar_menu_lateral(self)->str:
        with st.sidebar:
            st.header("Selecione a ação")
            opcao_selecionada:str=st.dropbox("Navegação",["Teste","teste","teste"])
            return opcao_selecionada
    
front=FrontEnd
front.renderizar_menu_lateral
    