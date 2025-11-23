# Sistema: Sistema de Livros (Título, Autor, Disponibilidade)
# Funcionalidades Obrigatórias: CRUD (Create,Read,Update,Delete), Resumo/Relatório, Sair
#   Funções com responsabilidades claras, tipo cadastrar_livro() apenas possuir cadastro, etc.
#   Uso de Listas de Dicionários (Dica: ter ID único para cada cadastro,validações simples,testar cada função separadamente.
#   Lista de dicionários: [{id: int, titulo: str,preco: float , autor: str, ano: int , disponivel:bool, quantidade: int}]
#
import json
import os
import typing

LivroDict = dict[str, int | str | bool | float]
ListaLivros = list[LivroDict]


class BackEnd:
    lista_livros: ListaLivros
    set_id: set[int]
    JSON_PATH = os.path.join(
        os.getcwd(), "projeto-final-python-alvaro-mariana/livros.json"
    )

    def __init__(self) -> None:
        self.lista_livros = []
        self.set_id = (
            set()
        )  # Set, pois 2 produtos diferentes não podem ter o mesmo código.
        self.set_titulo = set()  # 2 Livros diferentes não podem ter o mesmo nome, e também para permitir pesquisa por nome.
        self.carregar_dados()

    def carregar_dados(self) -> None:
        if not os.path.exists(self.JSON_PATH):
            with open(self.JSON_PATH, "w") as f:
                json.dump([], f)
            self.lista_livros = []
        try:
            with open(self.JSON_PATH, "r") as arquivo:
                try:
                    dados_json: ListaLivros = json.load(arquivo)
                    self.lista_livros = dados_json
                    for livro in self.lista_livros:
                        livro["id"] = int(livro["id"])
                        livro["titulo"] = str(livro["titulo"]).lower().strip()
                        livro["preco"] = float(
                            livro["preco"]
                        )  # Recomendável usar preço sem acento pra n dar BO
                        livro["autor"] = str(livro["autor"])
                        livro["ano"] = int(livro["ano"])
                        livro["quantidade"] = int(
                            livro["quantidade"]
                        )  # Coloquei quantidade antes de disponível pq irei ditar se é disponível pela quantidade.
                        livro["disponivel"] = (
                            livro["quantidade"] > 0
                        )  # Checa se é True ou False, se for >0 é true e estará automaticamente disponível, e vice-versa.
                        self.set_id.add(int(livro["id"]))
                        self.set_titulo.add(str(livro["titulo"]))
                except json.JSONDecodeError:
                    self.lista_livros = []
                    self.salvar_dados()
                    pass
        except FileNotFoundError:
            with open(self.JSON_PATH, "w") as f:
                json.dump([], f)
            self.lista_livros = []

    def salvar_dados(self) -> None:
        with open(self.JSON_PATH, "w") as arquivo:
            json.dump(self.lista_livros, arquivo)

    def obter_proximo_id(self) -> int:
        if self.set_id:
            return max(self.set_id)+1
        return 1
    def cadastrar_livro(
        self, titulo: str, preco: float, autor: str, ano: int, quantidade: int
    ) -> None:
        if not titulo or len(titulo.strip()) == 0:
            raise ValueError("Título não pode estar vazio!")
        if not autor or len(autor.strip()) == 0:
            raise ValueError("Autor não pode estar vazio!")
        if preco <= 0:
            raise ValueError("Valor deve ser maior que zero!")
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa!")
        if self.set_id:
            novo_id = max(self.set_id) + 1
        else:
            novo_id = 1
        if titulo.strip().lower() in self.set_titulo:
            raise ValueError(f"Título {titulo} já existente no sistema!")
        livro: dict[str, typing.Any] = {
            "id": int(novo_id),
            "titulo": str(titulo),
            "preco": float(preco),
            "autor": str(autor),
            "ano": int(ano),
            "disponivel": bool(quantidade > 0),
            "quantidade": int(quantidade),
        }
        self.lista_livros.append(livro)
        self.set_id.add(novo_id)
        self.set_titulo.add(titulo.strip().lower())
        self.salvar_dados()

    def atualizar_livro(
        self, id: int, campo: str, novo_valor: str | int | float
    ) -> None:
        if id not in self.set_id:
            raise ValueError("Código Inválido!")
        if len(campo) == 0:
            raise ValueError("Campo Inválido!")
        if isinstance(novo_valor, str) and len(novo_valor.strip()) == 0:
            raise ValueError("Novo Valor não pode estar vazio!")
        if campo.lower() in ["preco", "quantidade"]:
            if isinstance(novo_valor, (int, float)) and novo_valor < 0:
                raise ValueError("Valor não pode ser negativo!")
        for i in range(len(self.lista_livros)):
            if int(self.lista_livros[i]["id"]) == id:
                if campo.lower() == "titulo":
                    novo_titulo_form=str(novo_valor).strip().lower()
                    antigo_titulo_form=str(self.lista_livros[i]["titulo"]).strip().lower()
                    if novo_titulo_form != antigo_titulo_form and novo_titulo_form in self.set_titulo:
                        raise ValueError(f"Novo título {novo_valor} já existe para outro livro!")
                    if antigo_titulo_form in self.set_titulo:
                        self.set_titulo.remove(antigo_titulo_form)
                    self.set_titulo.add(novo_titulo_form)
                    self.lista_livros[i]["titulo"] = str(novo_valor)
                elif campo.lower() == "preco":
                    self.lista_livros[i]["preco"] = float(novo_valor)
                elif campo.lower() == "autor":
                    self.lista_livros[i]["autor"] = str(novo_valor)
                elif campo.lower() == "ano":
                    self.lista_livros[i]["ano"] = int(novo_valor)
                elif campo.lower() == "quantidade":
                    self.lista_livros[i]["quantidade"] = int(novo_valor)
                    self.lista_livros[i]["disponivel"] = int(novo_valor) > 0
                break
        self.salvar_dados()

    def buscar_livro(self, opcao: str, valor: str | int) -> list:
        resultados = []
        if opcao.lower() == "codigo":
            codigo = int(valor)
            if codigo not in self.set_id:
                raise ValueError("Livro não encontrado!")
            for livro in self.lista_livros:
                if livro["id"] == codigo:
                    resultados.append(livro)
                    break
        elif opcao.lower() == "titulo":
            for livro in self.lista_livros:
                if str(valor).lower() in str(livro["titulo"]).lower():
                    resultados.append(livro)
        elif opcao.lower() == "autor":
            for livro in self.lista_livros:
                if str(valor).lower() in str(livro["autor"]).lower():
                    resultados.append(livro)
        if not resultados:
            raise ValueError("Nenhum livro encontrado!")
        return resultados

    def excluir_livro(self, id: int) -> None:
        if id not in self.set_id:
            raise ValueError(f"Id {id} não encontrado! ")
        for i in range(len(self.lista_livros)):
            if int(self.lista_livros[i]["id"]) == id:
                _ = self.lista_livros.pop(i)
                self.set_id.remove(id)
                self.salvar_dados()
                break

    def listar_livros(self) -> ListaLivros:
        return self.lista_livros

    def gerar_relatorio(self) -> dict:
        total_livros = len(self.lista_livros)
        disponiveis = sum(1 for d in self.lista_livros if d["disponivel"])
        indisponiveis = total_livros - disponiveis
        valor_total = sum(float(d["preco"]) * int(d["quantidade"]) for d in self.lista_livros)
        return {
            "total_livros": total_livros,
            "livros_disponiveis": disponiveis,
            "livros_indisponiveis": indisponiveis,
            "valor_total_estoque": round(valor_total, 2),
        }
