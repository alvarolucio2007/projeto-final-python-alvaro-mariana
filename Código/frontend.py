# Esse é a part front-end do sistema, pra ficar mais organizado qualquer coisa avisa
# Lembra de fazer o seu venv (o meu ta no gitignore, que não é visto pelo git e github), e baixar o streamlit (pip install streamlit, ja com venv ativado)
import streamlit as st  # Fazer o front-end em si, para rodar, vai no terminal e digita "streamlit run {caminho relativo} "
from backend import BackEnd  # Importar o backend pra vc conseguir usar e testar aq
import pandas as pd

class FrontEnd:  # Recomendo fazer type hinting e POO pq fica chiquérrimo
    def __init__(self) -> None:
        self.backend = BackEnd()
        self.produtos = self.backend.lista_livros

    def exibir_mensagens_pendentes(
        self,
    ):  # Nos formulários, o streamlit gosta de resetar tudo com o st.rerun(), ent isso aq salva as mensagens de sucesso.
        if "success_message" in st.session_state:
            st.success(st.session_state["success_message"])
            del st.session_state["success_message"]

    def renderizar_menu_lateral(self) -> str:
        with st.sidebar:
            st.header("Selecione a ação")
            opcao_selecionada: str = st.radio(
                "",
                [
                    "Cadastrar Livro",
                    "Listar Livros",
                    "Buscar Livros",
                    "Atualizar Livros",
                    "Excluir Livros",
                    "Gerar Relatórios",
                ],
            )
            return opcao_selecionada

    def renderizar_cadastro(self) -> None:
        self.exibir_mensagens_pendentes()
        st.markdown("Cadastro de novo livro")
        with st.form("form_cadastro"):
            titulo = st.text_input("Título do Livro", max_chars=100)
            col1, col2 = st.columns(2)
            with col1:
                autor = st.text_input("Autor do Livro", max_chars=100)
            with col2:
                ano = st.number_input(
                    "Ano de lançamento", min_value=0, format="%d", step=1
                )
            col3, col4 = st.columns(2)
            with col3:
                preco = st.number_input(
                    "Preço do Livro", min_value=0.01, format="%.2f", step=0.01
                )
            with col4:
                quantidade = st.number_input(
                    "Quantidade do Livro", min_value=0, format="%d", step=1
                )
            clique_salvar = st.form_submit_button("Cadastrar e Salvar", width="stretch")
            if clique_salvar:
                try:
                    self.backend.cadastrar_livro(
                        titulo=str(titulo),
                        preco=float(preco),
                        autor=str(autor),
                        ano=int(ano),
                        quantidade=int(quantidade),
                    )
                    st.session_state["success_message"] = (
                        f"Produto '{titulo} adicionado com sucesso!"
                    )
                    st.rerun()
                except ValueError as e:
                    st.error(f"Falha no cadastro! {e}")
        return

    def renderizar_listar(self) -> None:
        st.title("Visão Geral do Estoque de Livros")
        try:
            st.dataframe(self.backend.lista_livros, width="stretch", hide_index=True)
        except Exception as e:
            print(f"Erro! {e}")

    def renderizar_buscar(self) -> None:
        st.markdown("Busca de Produto")
        tipo_busca = st.selectbox("Tipo de Busca", ("Código", "Título", "Autor"))
        if tipo_busca == "Código":
            busca = st.number_input("Qual seria o código?", min_value=0, step=1)
            if busca:
                resultados = self.backend.buscar_livro("codigo", busca)
                df_resultados = pd.DataFrame(resultados)
                if not df_resultados.empty:
                    st.success(f"Encontrado(s) {len(df_resultados)} produto(s).")
                    st.dataframe(df_resultados, width="stretch", hide_index=True)
                else:
                    st.warning(f"Nenhum produto encontrado com o código {busca}!")
        elif tipo_busca == "Título":
            busca = st.text_input("Qual seria o título?", max_chars=100)
            if busca:
                resultados = self.backend.buscar_livro("titulo", busca)
                df_resultados = pd.DataFrame(resultados)
                if not df_resultados.empty:
                    st.success(f"Encontrados {len(df_resultados)} produto(s).")
                    st.dataframe(df_resultados, width="stretch", hide_index=True)
                else:
                    st.warning(
                        f"Nenhum produto encontrado que inclui o título {busca}!"
                    )
        elif tipo_busca == "Autor":
            busca = st.text_input("Qual seria o autor?", max_chars=100)
            if busca:
                resultados = self.backend.buscar_livro("autor", busca)
                df_resultados = pd.DataFrame(resultados)
                if not df_resultados.empty:
                    st.success(f"Encontrados {len(df_resultados)} produto(s).")
                    st.dataframe(df_resultados, width="stretch", hide_index=True)
                else:
                    st.warning(
                        f"Nenhum produto encontrado que inclui o(a) autor(a) {busca}!"
                    )

    def renderizar_atualizar(self) -> None:
        st.markdown("Atualização de Produto")
        tipo_de_dado = st.selectbox(
            "Tipo de dado",
            ("Título", "Preço", "Autor", "Ano", "Quantidade"),
            key="upd_campo_select",
        )
        novo_valor = None
        with st.form("form_atualizar"):
            codigo = st.number_input("Código (ID)", min_value=1, step=1)
            if tipo_de_dado == "Preço":
                novo_valor = st.number_input(
                    "Qual seria o novo valor? ",
                    min_value=0.01,
                    step=0.01,
                    key="upd_valor_num",
                    format="%.2f",
                )
            elif tipo_de_dado in ("Título", "Autor"):
                novo_valor = st.text_input(
                    "Qual seria o novo valor? ", max_chars=100, key="upd_valor_str"
                )
            elif tipo_de_dado in ("Ano", "Quantidade"):
                novo_valor = st.number_input(
                    "Qual seria o novo valor?",
                    min_value=0,
                    step=1,
                    key="upd_valor_num",
                    format="%d",
                )
            clique_salvar = st.form_submit_button("Atualizar e Salvar", width="stretch")
            if clique_salvar:
                if novo_valor is None:
                    st.error("Erro! Por favor, insira o novo valor corretamente!")
                    return
                try:
                    self.backend.atualizar_livro(
                        id=int(codigo),
                        campo=tipo_de_dado.lower(),
                        novo_valor=novo_valor,
                    )
                except Exception as e:
                    st.error(f"Falha na atualização: {e}!")

    def renderizar_excluir(self) -> None:
        st.markdown("Excluir Livro")
        st.warning("Esta ação é permanente e não pode ser desfeita!")
        self.exibir_mensagens_pendentes()
        if "codigo_excluir" not in st.session_state:
            st.session_state.codigo_excluir = None
        with st.form("form_exclusao_busca"):
            codigo_excluir_input = st.number_input(
                "Insira o código (ID) do livro no qual deseja excluir: ",
                min_value=1,
                step=1,
                key="codigo_excluir_input_widget",
            )
            clique_buscar = st.form_submit_button(
                "Buscar produto para exclusão", width="stretch"
            )
            if clique_buscar:
                st.session_state.codigo_excluir = int(codigo_excluir_input)
                st.rerun()
        codigo_excluir = st.session_state.codigo_excluir
        if codigo_excluir and codigo_excluir in self.backend.set_id:
            titulo_gen = (
                livro["titulo"]
                for livro in self.backend.lista_livros
                if livro["id"] == codigo_excluir
            )
            titulo_produto = next(titulo_gen, "Livro não encontrado!")
            st.error(f"Você está prestes a excluir o produto: {titulo_produto}")
            clique_excluir = st.button("CONFIRMAR EXCLUSÃO", width="stretch")
            if clique_excluir:
                try:
                    self.backend.excluir_livro(int(codigo_excluir))
                    st.session_state["success_message"] = f"Livro {titulo_produto} excluído com sucesso!" # <--- Adicionar!
                    st.rerun()
                except Exception as e:
                    st.error(f"Falha na exclusão. Erro: {e}")
        elif (
            codigo_excluir is not None and codigo_excluir not in self.backend.set_id
        ):
            st.info(f"Nenhum produto encontrado com o código {int(codigo_excluir)}")
            st.session_state.codigo_excluir = None
        elif codigo_excluir is None:
            st.info("Digite um código e clique em buscar!")

    def renderizar_relatorios(self) -> None:
        st.title("Relatórios de estoque dos livros")
        livros=self.backend.lista_livros
        if not livros:
            st.info("Nenhum livro cadastrado para gerar relatórios.")
            return
        relatorio=self.backend.gerar_relatorio()
        col1,col2,col3,col4=st.columns(4)
        col1.metric("Total de títulos",relatorio["total_livros"])
        col2.metric("Livros disponíveis",relatorio["livros_disponiveis"])
        col3.metric("Livros indisponíveis",relatorio["livros_indisponiveis"])
        col4.metric("Valor total do estoque",relatorio["valor_total_estoque"])
        
        

    def rodar(self) -> None:
        opcao = self.renderizar_menu_lateral()
        if opcao == "Cadastrar Livro":
            self.renderizar_cadastro()
        elif opcao == "Listar Livros":
            self.renderizar_listar()
        elif opcao == "Buscar Livros":
            self.renderizar_buscar()
        elif opcao == "Atualizar Livros":
            self.renderizar_atualizar()
        elif opcao == "Excluir Livros":
            self.renderizar_excluir()
        elif opcao == "Gerar Relatórios":
            self.renderizar_relatorios()
        else:
            self.renderizar_listar()