import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from main import app

@pytest.mark.asyncio
async def test_adicionar_tarefa():
    mock_conn = AsyncMock()
    with patch("main.get_database", return_value=mock_conn):
        mock_conn.execute.return_value = None

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/tarefas/",
                json={"titulo": "Teste", "descricao": "Teste descrição", "concluida": False}
            )

        assert response.status_code == 201
        assert response.json() == {"message": "Tarefa adicionada com sucesso!"}
        mock_conn.execute.assert_called_once_with(
            "INSERT INTO tarefas (titulo, descricao, concluida) VALUES ($1, $2, $3)", 
            "Teste", "Teste descrição", False
        )

@pytest.mark.asyncio
async def test_listar_tarefas():
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = [
        {"id": 1, "titulo": "Teste 1", "descricao": "Descrição 1", "concluida": False},
        {"id": 2, "titulo": "Teste 2", "descricao": "Descrição 2", "concluida": True}
    ]
    with patch("main.get_database", return_value=mock_conn):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/tarefas/")

        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "titulo": "Teste 1", "descricao": "Descrição 1", "concluida": False},
            {"id": 2, "titulo": "Teste 2", "descricao": "Descrição 2", "concluida": True}
        ]
        mock_conn.fetch.assert_called_once_with("SELECT * FROM tarefas")

@pytest.mark.asyncio
async def test_buscar_tarefa():
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = {"id": 1, "titulo": "Teste", "descricao": "Teste descrição", "concluida": False}
    with patch("main.get_database", return_value=mock_conn):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/tarefas/1")

        assert response.status_code == 200
        assert response.json() == {"id": 1, "titulo": "Teste", "descricao": "Teste descrição", "concluida": False}
        mock_conn.fetchrow.assert_called_once_with("SELECT * FROM tarefas WHERE id = $1", 1)

@pytest.mark.asyncio
async def test_buscar_tarefa_nao_encontrada():
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None
    with patch("main.get_database", return_value=mock_conn):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/tarefas/999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Tarefa não encontrada."}
        mock_conn.fetchrow.assert_called_once_with("SELECT * FROM tarefas WHERE id = $1", 999)

@pytest.mark.asyncio
async def test_atualizar_tarefa():
    mock_conn = AsyncMock()
    with patch("main.get_database", return_value=mock_conn):
        mock_conn.execute.return_value = None

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.patch(
                "/api/v1/tarefas/1",
                json={"titulo": "Novo título", "descricao": None, "concluida": True}
            )

        assert response.status_code == 200
        assert response.json() == {"message": "Tarefa atualizada com sucesso!"}
        mock_conn.execute.assert_called_once_with(
            "UPDATE tarefas SET titulo = COALESCE($1, titulo), descricao = COALESCE($2, descricao), concluida = COALESCE($3, concluida) WHERE id = $4",
            "Novo título", None, True, 1
        )

@pytest.mark.asyncio
async def test_excluir_tarefa():
    mock_conn = AsyncMock()
    with patch("main.get_database", return_value=mock_conn):
        mock_conn.execute.return_value = None

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete("/api/v1/tarefas/1")

        assert response.status_code == 200
        assert response.json() == {"message": "Tarefa excluída com sucesso!"}
        mock_conn.execute.assert_called_once_with("DELETE FROM tarefas WHERE id = $1", 1)

@pytest.mark.asyncio
async def test_excluir_tarefa_nao_existe():
    mock_conn = AsyncMock()
    mock_conn.execute.return_value = None
    with patch("main.get_database", return_value=mock_conn):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete("/api/v1/tarefas/999")

        assert response.status_code == 200
        assert response.json() == {"message": "Tarefa excluída com sucesso!"}
        mock_conn.execute.assert_called_once_with("DELETE FROM tarefas WHERE id = $1", 999)

@pytest.mark.asyncio
async def test_adicionar_tarefa_invalida():
    mock_conn = AsyncMock()
    with patch("main.get_database", return_value=mock_conn):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/tarefas/",
                json={"descricao": "Faltou o título", "concluida": False}  # Falta o campo obrigatório 'titulo'
            )

        assert response.status_code == 422  # Código de erro para dados inválidos
        assert "titulo" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_listar_tarefas_vazia():
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = []  # Nenhuma tarefa no banco
    with patch("main.get_database", return_value=mock_conn):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/tarefas/")

        assert response.status_code == 200
        assert response.json() == []  # Lista vazia retornada
        mock_conn.fetch.assert_called_once_with("SELECT * FROM tarefas")
