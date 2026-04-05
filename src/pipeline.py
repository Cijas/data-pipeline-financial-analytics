"""
Financial Data Pipeline Orchestrator
=====================================

Main pipeline that orchestrates ingestion, transformation, and storage.
Implements a three-layer data architecture: Raw → Trusted → Refined

Author: Lucas
Date: 2024
"""

import logging
from datetime import datetime
from pathlib import Path

from ingestion import FinancialDataIngestion
from transformation import FinancialDataTransformer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FinancialPipeline:
    """
    Orchestrates the complete financial data pipeline.

    Architecture:
    ┌─────────────────────────────────────────────────────┐
    │ RAW LAYER (Ingestion)                               │
    │ - CSV/API data as-is                                │
    │ - Minimal validation                                │
    └────────────────────┬────────────────────────────────┘
                         │
    ┌────────────────────▼─────────────────────────────────┐
    │ TRUSTED LAYER (Cleaning & Enrichment)               │
    │ - Cleaned, validated data                            │
    │ - Business logic applied                             │
    │ - Quality checks passed                              │
    └────────────────────┬─────────────────────────────────┘
                         │
    ┌────────────────────▼─────────────────────────────────┐
    │ REFINED LAYER (Aggregation & Analytics)            │
    │ - Aggregated metrics                                 │
    │ - Ready for BI/Analytics                             │
    │ - Business KPIs                                      │
    └─────────────────────────────────────────────────────┘
    """

    def __init__(self, base_path: str = "../data"):
        """
        Initialize pipeline.

        Args:
            base_path: Base path for data directories
        """
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.processed_path = self.base_path / "processed"

        # Create directories
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)

        self.ingestion = FinancialDataIngestion(str(self.base_path))
        self.transformer = FinancialDataTransformer()

        self.execution_time = None
        self.status = "pending"

    def run(self, source: str = "mock", n_transactions: int = 100000) -> dict:
        """
        Execute the complete pipeline.

        Args:
            source: Data source ("mock" or "csv")
            n_transactions: Number of transactions to ingest

        Returns:
            Dictionary with pipeline results and metrics
        """
        start_time = datetime.now()

        logger.info("╔" + "═"*78 + "╗")
        logger.info("║" + " "*20 + "FINANCIAL DATA PIPELINE - EXECUTION START" + " "*16 + "║")
        logger.info("╚" + "═"*78 + "╝")

        try:
            # ========== STAGE 1: RAW LAYER ==========
            logger.info("\n" + "─"*80)
            logger.info("STAGE 1: RAW LAYER (Ingestion)")
            logger.info("─"*80)

            raw_df = self.ingestion.ingest(source=source, n_transactions=n_transactions)
            logger.info(f"✓ Raw data ingested | Shape: {raw_df.shape}")

            # ========== STAGE 2: TRUSTED LAYER ==========
            logger.info("\n" + "─"*80)
            logger.info("STAGE 2: TRUSTED LAYER (Cleaning & Enrichment)")
            logger.info("─"*80)

            transactions, customers, categories = self.transformer.transform(raw_df)
            logger.info(f"✓ Transactions cleaned | Shape: {transactions.shape}")
            logger.info(f"✓ Customer metrics created | Shape: {customers.shape}")
            logger.info(f"✓ Category metrics created | Shape: {categories.shape}")

            # ========== STAGE 3: REFINED LAYER (Storage) ==========
            logger.info("\n" + "─"*80)
            logger.info("STAGE 3: REFINED LAYER (Storage in Parquet)")
            logger.info("─"*80)

            # Save as Parquet (more efficient than CSV, used in real data lakes)
            transactions_path = self.processed_path / "transactions.parquet"
            customers_path = self.processed_path / "customer_metrics.parquet"
            categories_path = self.processed_path / "category_metrics.parquet"

            transactions.to_parquet(transactions_path, index=False)
            customers.to_parquet(customers_path, index=False)
            categories.to_parquet(categories_path, index=False)

            logger.info(f"✓ Transactions saved | Path: {transactions_path}")
            logger.info(f"✓ Customer metrics saved | Path: {customers_path}")
            logger.info(f"✓ Category metrics saved | Path: {categories_path}")

            # ========== DATA QUALITY METRICS ==========
            logger.info("\n" + "─"*80)
            logger.info("DATA QUALITY METRICS")
            logger.info("─"*80)

            quality_metrics = {
                "raw_records": len(raw_df),
                "trusted_records": len(transactions),
                "data_loss_percent": (
                    (len(raw_df) - len(transactions)) / len(raw_df) * 100
                ),
                "unique_customers": len(customers),
                "unique_categories": len(categories),
                "date_range": (
                    f"{transactions['transaction_date'].min().date()} to "
                    f"{transactions['transaction_date'].max().date()}"
                ),
                "total_volume": f"${transactions['amount'].sum():,.2f}",
                "avg_transaction": f"${transactions['amount'].mean():,.2f}"
            }

            for metric, value in quality_metrics.items():
                logger.info(f"  {metric}: {value}")

            # ========== COMPLETION ==========
            self.execution_time = (datetime.now() - start_time).total_seconds()
            self.status = "success"

            logger.info("\n" + "╔" + "═"*78 + "╗")
            logger.info("║" + " "*25 + "PIPELINE EXECUTION COMPLETED SUCCESSFULLY" + " "*11 + "║")
            logger.info(f"║ Total execution time: {self.execution_time:.2f} seconds" + " "*25 + "║")
            logger.info("╚" + "═"*78 + "╝\n")

            return {
                "status": "success",
                "execution_time_seconds": self.execution_time,
                "quality_metrics": quality_metrics,
                "output_files": {
                    "transactions": str(transactions_path),
                    "customer_metrics": str(customers_path),
                    "category_metrics": str(categories_path)
                }
            }

        except Exception as e:
            self.status = "failed"
            logger.error(f"❌ Pipeline execution failed: {str(e)}", exc_info=True)
            return {
                "status": "failed",
                "error": str(e),
                "execution_time_seconds": (datetime.now() - start_time).total_seconds()
            }


# Example usage
if __name__ == "__main__":
    # Initialize and run pipeline
    pipeline = FinancialPipeline(base_path="./data")

    # Run with mock data
    results = pipeline.run(source="mock", n_transactions=100000)

    # Print results
    print("\n" + "="*80)
    print("PIPELINE RESULTS")
    print("="*80)
    print(f"Status: {results['status']}")
    print(f"Execution time: {results['execution_time_seconds']:.2f}s")

    if results['status'] == 'success':
        print("\nOutput files:")
        for file_type, path in results['output_files'].items():
            print(f"  - {file_type}: {path}")
