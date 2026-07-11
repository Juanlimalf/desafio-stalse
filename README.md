# Desafio Stalse

## Sobre esse desafio

Esse repositório é a minha solução para o desafio técnico da Stalse, organizada em 4 fluxos simples:

1. **Dados** → pandas transforma um dataset do Kaggle em métricas agregadas.
2. **Backend** → expõe essas métricas e gerencia tickets de atendimento.
3. **Notificação** → ao fechar/priorizar um ticket, um webhook aciona um workflow no n8n.
4. **Frontend** → consome a API do backend.

Para as métricas, escolhi o dataset [NVIDIA GPU Sales (Synthetic 2026)](https://www.kaggle.com/datasets/uditjain13/nvidia-gpu-sales-synthetic-2026), baixei o CSV bruto e o transformei em um JSON de métricas agregadas (receita por família de GPU, região, canal de venda, segmento de cliente, tendência mensal etc.). Esse JSON é lido pelo [backend](backend/README.md), que disponibiliza os dados na rota `GET /metrics/` e também expõe as rotas de gerenciamento de tickets — ao fechar ou priorizar um ticket, ele dispara um webhook para um workflow no [n8n](n8n/README.md), que roteia a notificação por canal de atendimento. O [frontend](frontend/README.md) (Next.js + Flowbite React) fecha o ciclo, consumindo essa mesma API para exibir e gerenciar os tickets e visualizar as métricas.



Projeto composto por 4 partes, cada uma com seu próprio README detalhado:

| Pasta | O que é | README |
|-------|---------|--------|
| [`backend/`](backend) | API em FastAPI para gestão de tickets de atendimento (com webhook de notificação) e consulta de métricas de vendas. | [backend/README.md](backend/README.md) |
| [`data/`](data) | Script de ETL (pandas) que transforma o dataset bruto de vendas de GPUs NVIDIA (Kaggle) em `processed/metrics.json`, consumido pelo backend. | [data/readme.md](data/readme.md) |
| [`n8n/`](n8n) | Workflow n8n (via Docker) que recebe o webhook do backend e simula o roteamento da notificação por canal de atendimento (whatsapp, email, chat, telefone, instagram). | [n8n/readme.md](n8n/readme.md) |
| [`frontend/`](frontend) | Aplicação Next.js (com Flowbite React) que consome a API do backend para gerenciar tickets e visualizar as métricas de vendas. | [frontend/README.md](frontend/README.md) |

## Como os componentes se conectam

```
data/  --(ETL: etl.py)-->  data/processed/metrics.json  --(lido em runtime)-->  backend  GET /metrics/
                                                                                     │
                                                                                     ├── GET/PATCH /tickets  (SQLite: tickets.db)
                                                                                     │
                                                                                     └── ao fechar/priorizar um ticket, chama o
                                                                                          webhook cadastrado via POST /tickets/webhook
                                                                                                │
                                                                                                ▼
                                                                                            n8n (Channel Switch por canal do ticket)

frontend  --(consome a API REST)-->  backend
```

## Ordem sugerida para rodar tudo localmente

1. **Data**: gerar as métricas (`cd data && uv run python etl.py`, ou ver [data/README.md](data/README.md));
2. **Backend**: subir a API (`cd backend && uv sync && uv run uvicorn app.main:app --reload`, ou ver [backend/README.md](backend/README.md)) — em `http://127.0.0.1:8000` (docs em `/docs`);
3. **n8n** *(opcional, só para testar o fluxo de webhook)*: `cd n8n && docker compose up -d`, importar `workflow.json` e cadastrar a URL do webhook via `POST /tickets/webhook` (ver [n8n/README.md](n8n/README.md));
4. **Frontend**: `cd frontend && npm install && npm run dev` — em `http://localhost:3000` (ver [frontend/README.md](frontend/README.md)).

Cada subpasta tem seu próprio README com o passo a passo completo, pré-requisitos e detalhes de implementação.
