#Sistema: Sistema de Livros (Título, Autor, Disponibilidade)
#Funcionalidades Obrigatórias: CRUD (Create,Read,Update,Delete), Resumo/Relatório, Sair
#   Funções com responsabilidades claras, tipo cadastrar_livro() apenas possuir cadastro, etc.
#   Uso de Listas de Dicionários (Dica: ter ID único para cada cadastro,validações simples,testar cada função separadamente.
#   Lista de dicionários: [{id: int, titulo: str,preco: float , autor: str, ano: int , disponivel:bool, quantidade: int}]
# 
import json
import streamlit as st
import os

LivroDict=dict[str,int|str|bool|float]
ListaLivros=list[LivroDict]

class BackEnd():
    lista_livros:ListaLivros
    set_id:set[int]
    JSON_PATH = os.path.join(os.getcwd(), "livros.json")
    def __init__(self) -> None:
        self.lista_livros = []
        self.set_id = set() #Set, pois 2 produtos diferentes não podem ter o mesmo código.
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