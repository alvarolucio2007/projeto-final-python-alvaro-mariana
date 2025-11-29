# 📚 Sistema de Gerenciamento de Livros (CRUD)

![Status](https://img.shields.io/badge/Status-Pronto%20para%20Frontend-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red)
![Architecture](https://img.shields.io/badge/Architecture-POO%2FTyped-orange)

> Um sistema de gerenciamento de estoque de livros (Título, Autor, Disponibilidade) dividido em camadas **Backend (Lógica de Negócio)** e **Frontend (Interface Streamlit)**. Este módulo (`backend.py`) é o coração do sistema, responsável por toda a gestão de dados.

---

## 🖼️ Preview
*(Sua colega deve adicionar aqui um screenshot ou GIF da interface Streamlit)*
![Screenshot do App](https://via.placeholder.com/800x400?text=Frontend+em+Streamlit)

---

## 🌟 Arquitetura e Destaques Técnicos

O projeto foi construído seguindo o princípio de **separação de responsabilidades (POO)** e a busca por código de alta qualidade:

1.  **Backend (Classe `BackEnd`):**
    * **Programação Orientada a Objetos (POO):** Toda a lógica de negócio (CRUD, validações, relatórios) e a persistência de dados estão encapsuladas nesta classe.
    * **Tipagem Forte (Type Hinting):** Uso de `typing` e `type aliases` (`ListaLivros`, `LivroDict`) em todos os métodos para garantir a integridade dos dados e facilitar a manutenção.
    * **Integridade de Dados:** Utiliza `set`s (`set_id`, `set_titulo`) para garantir que o **ID** e o **Título** de cada livro sejam sempre únicos.

2.  **Persistência de Dados:** Os dados são salvos de forma assíncrona no arquivo **`livros.json`**, garantindo que o estado do sistema seja mantido entre as sessões.

---

## 🚀 Funcionalidades do Backend

A classe `BackEnd` (`backend.py`) fornece os seguintes métodos principais para serem consumidos pela interface (Streamlit):

| Método | Responsabilidade |
| :--- | :--- |
| `cadastrar_livro()` | Insere um novo registro com validações de dados e unicidade. |
| `listar_livros()` | Retorna a lista completa de livros no estoque. |
| `buscar_livro()` | Retorna resultados filtrados por Código (ID), Título ou Autor. |
| `atualizar_livro()` | Modifica campos específicos de um livro (e recalcula a disponibilidade). |
| `excluir_livro()` | Remove um livro pelo ID e mantém os conjuntos de unicidade sincronizados. |
| `gerar_relatorio()` | Gera um dicionário com estatísticas rápidas do estoque. |

---

## 📂 Estrutura do Projeto

O código de lógica está segregado da interface, facilitando o desenvolvimento paralelo e a manutenção:

```text
📁 sistema-livros
├── 📄 app.py              # <--- Frontend (Interface do Usuário com Streamlit)
├── 📄 backend.py          # <--- Backend (Lógica POO e CRUD)
├── 📄 livros.json         # Arquivo de persistência de dados
├── 📄 requirements.txt    # Dependências do projeto (incluir Streamlit aqui)
└── 📄 README.md           # Este arquivo
```
## ⚙️ Como Executar

O sistema é construído em Python 3.12.3 e utiliza o framework Streamlit para o Frontend.

### 1. Requisitos e Setup
```bash
# Clone o repositório
git clone [https://docs.github.com/pt/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github](https://docs.github.com/pt/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
cd sistema-livros

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate