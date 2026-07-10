# Desafio Stalse — Backend

API em **FastAPI** para o desafio Stalse. Expõe:

- Gestão de **tickets** de atendimento (listagem, atualização de status/prioridade e cadastro de webhook de notificação);
- Consulta de **métricas** de vendas geradas pelo pipeline de dados do projeto (pasta [`data/`](../data)).

## Stack

- Python 3.13
- FastAPI + Uvicorn
- SQLAlchemy assíncrono (`aiosqlite`) — persistência dos tickets em `tickets.db` (SQLite)
- httpx — chamadas de webhook

## Pré-requisitos

- Python 3.13 instalado (ver [`.python-version`](.python-version));
- Para as métricas funcionarem, o arquivo `data/processed/metrics.json` precisa existir — ele é gerado pelo ETL em [`data/etl.py`](../data/etl.py).

## Como executar

O projeto já vem com `pyproject.toml`/`uv.lock` (gerenciado com [UV](https://docs.astral.sh/uv/)) e também com `requirements.txt`/`requirements.dev.txt` exportados, para quem preferir pip puro.

### Opção 1 — com UV (recomendado)

```bash
# instala as dependências (runtime + dev) em um venv local .venv
uv sync

# sobe a API com reload automático
uv run uvicorn app.main:app --reload

# alternativa: rodar o entrypoint diretamente
uv run python -m app.main
```

### Opção 2 — com Python + pip

```bash
# cria e ativa um virtualenv
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# instala dependências de runtime (e, opcionalmente, as de dev)
pip install -r requirements.txt
pip install -r requirements.dev.txt   # opcional: testes/lint

# sobe a API
uvicorn app.main:app --reload
# ou
python -m app.main
```

A API sobe por padrão em `http://127.0.0.1:8000`. Documentação interativa (Swagger) em `http://127.0.0.1:8000/docs`.

## Banco de dados e seed

Ao iniciar (`lifespan`), a aplicação:

1. Cria as tabelas no SQLite (`tickets.db`, na raiz do backend), caso não existam;
2. Popula a tabela de tickets a partir de [`tickets.json`](tickets.json), somente se ela estiver vazia.

Não é necessário nenhum setup manual de banco — tudo acontece automaticamente no startup.

## Testes

```bash
uv run pytest
# ou, com o venv ativo
pytest
```

## Rotas

### Tickets — `/tickets`

| Método | Rota                  | Descrição |
|--------|-----------------------|-----------|
| `POST` | `/tickets/webhook`     | Registra a URL que será chamada sempre que um ticket for atualizado com status `closed` ou prioridade `high`. |
| `GET`  | `/tickets/webhook`     | Retorna a URL do webhook atualmente cadastrada. Retorna `404` se nenhuma URL tiver sido registrada. |
| `GET`  | `/tickets/`            | Retorna todos os tickets cadastrados. |
| `PATCH`| `/tickets/{ticket_id}` | Atualiza `status` e/ou `priority` de um ticket. Se o resultado disparar a condição de notificação, o webhook cadastrado é chamado com os dados do ticket. |

Campos de ticket: `ticket_id`, `created_at`, `customer_name`, `channel` (`whatsapp`, `email`, `chat`, `telefone`, `instagram`), `subject`, `status` (`opened`, `closed`), `priority` (`low`, `medium`, `high`).

### Métricas — `/metrics`

| Método | Rota        | Descrição |
|--------|-------------|-----------|
| `GET`  | `/metrics/` | Lê `data/processed/metrics.json` (gerado pelo ETL) e retorna as métricas agregadas de vendas: período (`date_range`), total de registros, receita total, unidades vendidas e receita quebrada por família/modelo de GPU, região, canal de venda, segmento de cliente e tendência mensal. Retorna `404` se o arquivo de métricas não existir. |

## Estrutura do projeto

```
app/
├── main.py                  # cria a FastAPI app, registra middlewares e rotas
├── tickets/                 # domínio de tickets
│   ├── router/               # rotas + injeção de dependências
│   ├── service/               # regras de negócio (update, notificação de webhook)
│   ├── repository/             # acesso a dados (SQLAlchemy)
│   ├── model/                  # modelo ORM
│   └── schema/                 # schemas Pydantic (request/response)
├── metrics/                 # domínio de métricas
│   ├── router/
│   ├── service/               # leitura do metrics.json
│   └── schema/
└── shared/                  # infraestrutura comum (DB, http client, logger, middleware/lifespan)
```
