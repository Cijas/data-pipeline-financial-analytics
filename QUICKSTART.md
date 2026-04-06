# ⚡ Quick Start Guide

## 5 Minutes to Run the Complete Pipeline

### Prerequisites
- Python 3.10+ installed
- Git installed (optional)

---

## 🚀 Step by Step

### 1️⃣ Navigate to the folder
```bash
cd data-pipeline-financial-analytics
```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
```

### 3️⃣ Activate the environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Run the pipeline
```bash
cd src
python pipeline.py
```

### 6️⃣ View the results
Processed files will be in:
```
data/processed/
├── transactions.parquet
├── customer_metrics.parquet
└── category_metrics.parquet
```

---

## 📊 What does the pipeline generate?

### transactions.parquet (~5MB)
- 100K cleaned and enriched transactions
- 15+ columns including temporal features
- Ready for analysis

### customer_metrics.parquet (~500KB)
- 5K unique customers
- Total spending, frequency, categories
- First/last transaction dates

### category_metrics.parquet (~100KB)
- Monthly metrics by category
- Volume, revenue, trends
- Ready for dashboard

---

### Explore the data
```python
import pandas as pd

df = pd.read_parquet('data/processed/transactions.parquet')
print(df.head())
print(df.describe())
```

### Run more transactions
In `src/pipeline.py`, change:
```python
results = pipeline.run(source="mock", n_transactions=500000)
```

### Run SQL queries
Open file `sql/analytics_queries.sql` to see 8+ ready-to-run queries.

### Create a notebook
```bash
jupyter notebook notebooks/exploration.ipynb
```

---

## ❓ Troubleshooting

### Error: "module not found"
**Solution:** Make sure the virtual environment is activated:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "ModuleNotFoundError: No module named 'pandas'"
**Solution:** Install dependencies:
```bash
pip install pandas pyspark numpy python-dotenv
```

### Error: "Permission denied"
**Solution (Windows):** Run PowerShell as administrator

---

## 📈 Expected output example

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
  date_range: 2024-10-19 to 2026-04-04

╔══════════════════════════════════════════════════════════════════════════════╗
║                    PIPELINE EXECUTION COMPLETED SUCCESSFULLY                  ║
║ Total execution time: 2.45 seconds                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 💡 Tips

- **To understand the code:** Read `src/ingestion.py` first, then `transformation.py`, finally `pipeline.py`
- **To modify:** Each file has inline documentation in comments
- **To deploy:** See the "Production Deployment" section in README.md
- **For portfolio:** Publish on GitHub and add to your bio!

---

**Ready to impress! 🚀**
