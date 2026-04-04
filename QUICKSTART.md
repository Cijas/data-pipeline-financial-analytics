# ⚡ Quick Start Guide

## 5 Minutos para rodar o pipeline completo

### Pré-requisitos
- Python 3.10+ instalado
- Git instalado (opcional)

---

## 🚀 Passo a Passo

### 1️⃣ Navegue até a pasta
```bash
cd c:\Users\krndk\data-pipeline-financial-analytics
```

### 2️⃣ Crie um ambiente virtual
```bash
python -m venv venv
```

### 3️⃣ Ative o ambiente
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 5️⃣ Execute o pipeline
```bash
cd src
python pipeline.py
```

### 6️⃣ Veja os resultados
Os arquivos processados estarão em:
```
data/processed/
├── transactions.parquet
├── customer_metrics.parquet
└── category_metrics.parquet
```

---

## 📊 O que o pipeline gera?

### transactions.parquet (~5MB)
- 100K transações limpas e enriquecidas
- 15+ colunas incluindo features temporais
- Pronto para análise

### customer_metrics.parquet (~500KB)
- 5K clientes únicos
- Gasto total, frequência, categorias
- Datas de primeira/última transação

### category_metrics.parquet (~100KB)
- Métricas mensais por categoria
- Volume, receita, tendências
- Pronto para dashboard

---

## 🔥 Próximas ações

### Explorar os dados
```python
import pandas as pd

df = pd.read_parquet('data/processed/transactions.parquet')
print(df.head())
print(df.describe())
```

### Rodarmais transações (maior volume)
No arquivo `src/pipeline.py`, mude:
```python
results = pipeline.run(source="mock", n_transactions=500000)  # 500K ao invés de 100K
```

### Executar queries SQL
Abra o arquivo `sql/analytics_queries.sql` para ver 8+ queries prontas.
Adapte e rodeem seu banco SQL favorito.

### Criar notebook
```bash
jupyter notebook notebooks/exploration.ipynb
```

---

## ❓ Troubleshooting

### Erro: "module not found"
**Solução:** Certifique-se que o ambiente virtual está ativado:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Erro: "ModuleNotFoundError: No module named 'pandas'"
**Solução:** Instale as dependências:
```bash
pip install pandas pyspark numpy python-dotenv
```

### Erro: "Permission denied"
**Solução (Windows):** Execute PowerShell como administrador

---

## 📈 Exemplo de output esperado

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FINANCIAL DATA PIPELINE - EXECUTION START                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

────────────────────────────────────────────────────────────────────────────────
STAGE 1: RAW LAYER (Ingestion)
────────────────────────────────────────────────────────────────────────────────
    Generating 100,000 mock transactions...
    Generated 100,000 transactions

────────────────────────────────────────────────────────────────────────────────
STAGE 2: TRUSTED LAYER (Cleaning & Enrichment)
────────────────────────────────────────────────────────────────────────────────
    Starting data cleaning...
    Cleaned data shape: (99500, 15)
    Enriching transaction data...
    Aggregating customer metrics...
    Aggregating category metrics...

────────────────────────────────────────────────────────────────────────────────
STAGE 3: REFINED LAYER (Storage)
────────────────────────────────────────────────────────────────────────────────
    ✓ Transactions saved
    ✓ Customer metrics saved
    ✓ Category metrics saved

─────────────────────────────────────────────────────────────────────────────────
DATA QUALITY METRICS
─────────────────────────────────────────────────────────────────────────────────
  raw_records: 100000
  trusted_records: 99500
  data_loss_percent: 0.5
  unique_customers: 5000
  unique_categories: 6
  date_range: 2024-10-19 to 2025-04-04

╔══════════════════════════════════════════════════════════════════════════════╗
║                    PIPELINE EXECUTION COMPLETED SUCCESSFULLY                  ║
║ Total execution time: 2.45 seconds                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 💡 Dicas

- **Para entender o código:** Leia primeiro `src/ingestion.py`, depois `transformation.py`, finalmente `pipeline.py`
- **Para modificar:** Cada arquivo tem documentação inline nos comentários
- **Para deployar:** Veja a seção "Production Deployment" no README.md
- **Para portfólio:** Publique no GitHub e adicione à sua bio!

---

**Pronto para impressionar! 🚀**
