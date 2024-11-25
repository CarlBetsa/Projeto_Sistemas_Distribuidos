# Criando um arquivo README.md com o conteúdo gerado

readme_content = """
# To-Do List Application 📝

Este é um sistema de **To-Do List** desenvolvido usando **Flask** como frontend, **FastAPI** como backend e **PostgreSQL** como banco de dados. O projeto foi configurado para ser executado em contêineres Docker, facilitando a implantação e o uso.

## 📋 Funcionalidades

- **Adicionar tarefas** com título e descrição.
- **Listar tarefas** existentes.
- **Editar tarefas** (título, descrição e status de conclusão).
- **Excluir tarefas**.
- Persistência de dados no banco de dados PostgreSQL.

---

## 🛠️ Tecnologias Utilizadas

- **Frontend:** Flask
- **Backend:** FastAPI
- **Banco de Dados:** PostgreSQL
- **Docker:** Para orquestração de contêineres
- **Uvicorn:** Servidor ASGI para FastAPI

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

1. **Docker e Docker Compose** instalados no sistema:
   - [Instalar Docker](https://docs.docker.com/get-docker/)
   - [Instalar Docker Compose](https://docs.docker.com/compose/install/)

2. **Clonar o repositório**:
   ```bash
   git clone https://github.com/CarlBetsa/Projeto_Sistemas_Distribuidos.git
   cd Projeto_Sistemas_Distribuidos
   ```
3. **Suba os serviços usando Docker Compose** com o Docker aberto no seu computador rode o comando:
    ```bash
    docker-compose up --build
    ```
4. Verifique os serviços rodando:

    Frontend Flask: http://localhost:3000

    Backend FastAPI: http://localhost:8000/docs