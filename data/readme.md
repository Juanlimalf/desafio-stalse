# Desafio Stalse — Data / ETL

Script de ETL que transforma o dataset bruto de vendas de GPUs NVIDIA em um JSON de métricas agregadas, consumido pela rota `GET /metrics/` do [backend](../backend).

Fonte do dataset: https://www.kaggle.com/datasets/uditjain13/nvidia-gpu-sales-synthetic-2026

## Stack

- Python 3.14
- pandas — leitura e agregação do CSV

## Pré-requisitos

- Python 3.14 instalado (ver [`.python-version`](.python-version));
- O arquivo bruto já está versionado em [`raw/nvidia_gpu_sales_synthetic_2026.csv`](raw/nvidia_gpu_sales_synthetic_2026.csv) (7000 registros de vendas).

## Como executar

O projeto é gerenciado com [UV](https://docs.astral.sh/uv/) (`pyproject.toml`/`uv.lock`), mas também pode ser rodado com um ambiente Python simples.

### Opção 1 — com UV (recomendado)

```bash
# instala as dependências em um venv local .venv
uv sync

# roda o ETL
uv run python etl.py
```

### Opção 2 — com Python + pip

```bash
# cria e ativa um virtualenv
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# instala as dependências (não há requirements.txt, instale diretamente)
pip install pandas

# roda o ETL
python etl.py
```

## O que o ETL faz

[`etl.py`](etl.py):

1. Lê `raw/nvidia_gpu_sales_synthetic_2026.csv` com pandas, convertendo `sale_date` para datetime;
2. Calcula, sobre o dataset inteiro:
   - `date_range`: data mínima e máxima de venda;
   - `total_records`: quantidade de linhas;
   - `total_revenue_usd` / `total_units_sold`: receita e unidades totais;
   - `revenue_by_gpu_family`, `revenue_by_region`, `revenue_by_sales_channel`, `revenue_by_customer_segment`, `revenue_by_gpu_model`: receita agrupada e ordenada de forma decrescente por cada dimensão;
   - `monthly_revenue_trend`: receita somada por mês (`YYYY-MM`);
3. Grava o resultado em `processed/metrics.json` (cria a pasta `processed/` se não existir).

Esse `metrics.json` é o arquivo que o backend lê em tempo de requisição — sempre que o dataset bruto mudar, basta rodar o ETL novamente para atualizar as métricas expostas pela API.

## Estrutura

```
data/
├── etl.py               # script de transformação CSV -> JSON
├── raw/
│   └── nvidia_gpu_sales_synthetic_2026.csv   # dataset bruto (fonte: Kaggle)
└── processed/
    └── metrics.json      # saída consumida por app/metrics no backend
```
