#Sistema: Sistema de Livros (Título, Autor, Disponibilidade)
#Funcionalidades Obrigatórias: CRUD (Create,Read,Update,Delete), Resumo/Relatório, Sair
#   Funções com responsabilidades claras, tipo cadastrar_livro() apenas possuir cadastro, etc.
#   Uso de Listas de Dicionários (Dica: ter ID único para cada cadastro,validações simples,testar cada função separadamente.
#   Lista de dicionários: [{id: int, titulo: str,preco: float , autor: str, ano: int , disponivel:bool, quantidade: int}]
#
import json
import typing
import os

LivroDict=dict[str,int|str|bool|float]
ListaLivros=list[LivroDict]

class BackEnd():
    lista_livros:ListaLivros
    set_id:set[int]
    JSON_PATH = os.path.join(os.getcwd(), "projeto-final-python-alvaro-mariana/livros.json")
    def __init__(self) -> None:
        self.lista_livros = []
        self.set_id = set() #Set, pois 2 produtos diferentes não podem ter o mesmo código.
        self.set_titulo = set() #2 Livros diferentes não podem ter o mesmo nome, e também para permitir pesquisa por nome.
        self.carregar_dados()
    def carregar_dados(self) -> None:
        if not os.path.exists(self.JSON_PATH):
            with open(self.JSON_PATH,"w") as f:
                json.dump([],f)
            self.lista_livros=[]
        try:
            with open(self.JSON_PATH,"r") as arquivo:
                try:
                    dados_json: ListaLivros = json.load(arquivo)
                    self.lista_livros=dados_json
                    for livro in self.lista_livros:
                        livro["id"] = int(livro["id"])
                        livro["titulo"] = str(livro["titulo"])
                        livro["preco"] = float(livro["preco"]) #Recomendável usar preço sem acento pra n dar BO
                        livro["autor"] = str(livro["autor"])
                        livro["ano"] = int(livro["ano"])
                        livro["quantidade"] = int(livro["quantidade"]) #Coloquei quantidade antes de disponível pq irei ditar se é disponível pela quantidade.
                        livro["disponivel"]=livro["quantidade"]>0 #Checa se é True ou False, se for >0 é true e estará automaticamente disponível, e vice-versa.
                        self.set_id.add(int(livro["id"]))
                        self.set_titulo.add(str(livro["titulo"]))
                except json.JSONDecodeError:
                    self.lista_livros=[]
                    self.salvar_dados()
                    pass
        except FileNotFoundError:
            with open(self.JSON_PATH, "w") as f:
                json.dump([],f)
            self.lista_livros=[]
    def salvar_dados(self) -> None:
        with open(self.JSON_PATH, "w") as arquivo:
            json.dump(self.lista_livros, arquivo)
    def cadastrar_livro(self,titulo:str,preco:float,autor:str,ano:int,quantidade:int) -> None:
        if not titulo or len(titulo.strip())==0:
            raise ValueError("Título não pode estar vazio!")
        if not autor or len(autor.strip())==0:
            raise ValueError("Autor não pode estar vazio!")
        if preco<=0:
            raise ValueError("Valor deve ser maior que zero!")
        if quantidade<0:
            raise ValueError("Quantidade não pode ser negativa!")
        if self.set_id:
            novo_id=max(self.set_id)+1
        else:
            novo_id=1
        livro: dict[str,typing.Any]={
            "id":int(novo_id),
            "titulo":str(titulo),
            "preco":float(preco),
            "autor":str(autor),
            "ano":int(ano),
            "disponivel": bool(quantidade>0),
            "quantidade": int(quantidade)
        }
        self.lista_livros.append(livro)
        self.set_id.add(novo_id)
        self.set_titulo.add(titulo)
        self.salvar_dados()
    def atualizar_livro(self,codigo:int, campo:str, novo_valor :str|int|float) -> None:
        if id not in self.set_id:
            raise ValueError("Código Inválido!")
        if len(campo)==0:
            raise ValueError("Campo Inválido!")
        if isinstance(novo_valor,int) or isinstance(novo_valor,str) and  len(novo_valor)==0:
            raise ValueError("Novo Valor Inválido!")
        for i in range(len(self.lista_livros)):
            if campo.lower()=="nome":
                self.lista_livros[i]["Nome"]=str(novo_valor)
            elif campo.lower()==""