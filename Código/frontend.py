#Esse é a part front-end do sistema, pra ficar mais organizado qualquer coisa avisa
#Lembra de fazer o seu venv (o meu ta no gitignore, que não é visto pelo git e github), e baixar o streamlit (pip install streamlit, ja com venv ativado)
import streamlit as st #Fazer o front-end em si, para rodar, vai no terminal e digita "streamlit run {caminho relativo} "
from backend import BackEnd #Importar o backend pra vc conseguir usar e testar aq
class FrontEnd: #Recomendo fazer type hinting e POO pq fica chiquérrimo
    def __init__(self) -> None:
        self.estoque=BackEnd()
        self.produtos=self.estoque.lista_livros
    def exibir_mensagens_pendentes(self): #Nos formulários, o streamlit gosta de resetar tudo com o st.rerun(), ent isso aq salva as mensagens de sucesso.
        if 'success_message' in st.session_state:
            st.success(st.session_state['success_message'])
            del st.session_state['success_message']
    def renderizar_menu_lateral(self)->str:
        with st.sidebar:
            st.header("Selecione a ação")
            opcao_selecionada:str=st.selectbox("Navegação",["Cadastrar Livro","Listar Livros","Buscar Livros","Atualizar Livros","Excluir Livros","Gerar Relatórios"])
            return opcao_selecionada
    def renderizar_cadastro(self) -> None:
        self.exibir_mensagens_pendentes()
        st.markdown("Cadastro de novo livro")
        with st.form("form_cadastro"):
            titulo=st.text_input("Título do Livro",max_chars=100)
            col1,col2=st.columns(2)
            with col1:
                autor=st.text_input("Autor do Livro",max_chars=100)
            with col2:
                ano=st.number_input("Ano de lançamento",min_value=0,format="%d",step=1)
            col3,col4=st.columns(2)
            with col3:
                preco=st.number_input("Preço do Livro",min_value=0.01,format="%.2f",step=0.01)
            with col4:
                quantidade=st.number_input("Quantidade do Livro",min_value=0,format="%d",step=1)
            clique_salvar=st.form_submit_button("Cadastrar e Salvar", width='stretch')
            if clique_salvar:
                try:
                    self.estoque.cadastrar_livro(
                        titulo=str(titulo),
                        preco=float(preco),
                        autor=str(autor),
                        ano=int(ano),
                        quantidade=int(quantidade)
                    )
                    
                    st.session_state['success_message']=f"Produto '{titulo} adicionado com sucesso!"
                    st.rerun()
                except ValueError as e:
                    st.error(f"Falha no cadastro! {e}")
        return
    def renderizar_atualizar(self)-> None:
        pass
                    
if __name__=="__main__":
    app=FrontEnd()
    app.renderizar_cadastro() #Mude essa função aq pra mudar oq aparece na pagina do streamlit

    #