"""
Data Ingestion Module
=====================

Handles ingestion of financial transaction data from various sources.
Supports CSV and API-based ingestion patterns.

Author: Data Engineering Team
Date: April 2026
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialDataIngestion:
    """Handles ingestion of financial transaction data."""

    def __init__(self, data_path: str):
        """
        Initialize ingestion module.

        Args:
            data_path: Path to raw data directory
        """
        self.data_path = Path(data_path)
        self.raw_dir = self.data_path / "raw"
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def generate_mock_transactions(
        self,
        n_transactions: int = 100000,
        n_customers: int = 5000,
        date_range: int = 180
    ) -> pd.DataFrame:
        """
        Generate mock financial transaction data.

        This is realistic data for testing the pipeline in development.
        In production, this would be replaced by actual API/database calls.

        Args:
            n_transactions: Number of transactions to generate
            n_customers: Number of unique customers
            date_range: Number of days of data to generate

        Returns:
            DataFrame with transaction data
        """
        logger.info("Generating %d mock transactions...", n_transactions)

        np.random.seed(42)

        # Generate base data
        customers = [f"CUST_{i:06d}" for i in range(n_customers)]
        categories = ["Food", "Entertainment", "Transportation", "Shopping", "Utilities", "Healthcare"]

        # Time range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=date_range)

        data = {
            "transaction_id": [f"TXN_{i:08d}" for i in range(n_transactions)],
            "customer_id": np.random.choice(customers, n_transactions),
            "transaction_date": [
                start_date + timedelta(days=np.random.randint(0, date_range))
                for _ in range(n_transactions)
            ],
            "amount": np.random.exponential(scale=150, size=n_transactions).round(2),
            "category": np.random.choice(categories, n_transactions),
            "merchant": [f"Merchant_{i%1000:04d}" for i in range(n_transactions)],
            "status": np.random.choice(["completed", "pending", "failed"], n_transactions, p=[0.85, 0.10, 0.05])
        }

        df = pd.DataFrame(data)

        logger.info("Generated %d transactions | Date range: %s to %s",
                    len(df), df['transaction_date'].min().date(),
                    df['transaction_date'].max().date())

        return df

    def load_from_csv(self, filename: str) -> pd.DataFrame:
        """Load transactions from CSV file."""
        filepath = self.raw_dir / filename
        logger.info("Loading data from %s", filepath)
        return pd.read_csv(filepath)

    def save_raw_data(self, df: pd.DataFrame, filename: str = "transactions.csv") -> str:
        """
        Save raw data to CSV.

        Args:
            df: DataFrame to save
            filename: Output filename

        Returns:
            Path to saved file
        """
        filepath = self.raw_dir / filename
        df.to_csv(filepath, index=False)
        logger.info("Raw data saved to %s | Shape: %s", filepath, df.shape)
        return str(filepath)

    def ingest(
        self,
        source: str = "mock",
        n_transactions: int = 100000
    ) -> pd.DataFrame:
        """
        Main ingestion method.

        Args:
            source: "mock" or "csv"
            n_transactions: Number of transactions (if using mock)

        Returns:
            Ingested DataFrame
        """
        if source == "mock":
            df = self.generate_mock_transactions(n_transactions=n_transactions)
        elif source == "csv":
            df = self.load_from_csv("transactions.csv")
        else:
            raise ValueError(f"Unknown source: {source}")

        self.save_raw_data(df)
        return df


# Example usage
if __name__ == "__main__":
    ingestion = FinancialDataIngestion("../data")
    df = ingestion.ingest(source="mock", n_transactions=100000)
    print(df.head())
    print(f"\nData shape: {df.shape}")
    print(f"\nData types:\n{df.dtypes}")
