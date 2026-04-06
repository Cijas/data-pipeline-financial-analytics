"""
Data Transformation Module
===========================

Core transformations for financial data pipeline.
Handles data cleaning, enrichment, and feature engineering.

Author: Data Engineering Team
Date: April 2026
"""

import logging
from typing import Tuple

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialDataTransformer:
    """Transforms raw financial data into trusted/refined layers."""

    def __init__(self):
        """Initialize transformer."""
        self.quality_metrics = {}

    def clean_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean transaction data.

        Operations:
        - Remove null values
        - Validate amounts > 0
        - Fix data types
        - Handle duplicates

        Args:
            df: Raw transaction DataFrame

        Returns:
            Cleaned DataFrame
        """
        logger.info("Starting data cleaning...")
        initial_rows = len(df)

        # Remove nulls
        df = df.dropna()
        logger.info(f"Removed null values: {initial_rows - len(df)} rows")

        # Remove negative amounts
        df = df[df["amount"] > 0]
        logger.info(f"Removed negative amounts: {len(df)} rows remaining")

        # Remove duplicates
        df = df.drop_duplicates(subset=["transaction_id"])

        # Fix data types
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        df["amount"] = df["amount"].astype(float)

        logger.info(f"Cleaned data shape: {df.shape}")

        return df

    def enrich_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrich transaction data with computed features.

        Adds:
        - Transaction hour, day, month, quarter
        - Amount brackets
        - Transaction velocity flags

        Args:
            df: Cleaned transaction DataFrame

        Returns:
            Enriched DataFrame
        """
        logger.info("Enriching transaction data...")

        # Temporal features
        df["transaction_hour"] = df["transaction_date"].dt.hour
        df["transaction_day"] = df["transaction_date"].dt.day
        df["transaction_month"] = df["transaction_date"].dt.month
        df["transaction_quarter"] = df["transaction_date"].dt.quarter
        df["transaction_year"] = df["transaction_date"].dt.year
        df["day_of_week"] = df["transaction_date"].dt.dayofweek
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

        # Amount brackets
        df["amount_bracket"] = pd.cut(
            df["amount"],
            bins=[0, 50, 100, 200, 500, float("inf")],
            labels=["micro", "small", "medium", "large", "xlarge"]
        )

        logger.info(f"Enriched data shape: {df.shape}")

        return df

    def aggregate_customer_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate metrics by customer.

        Metrics:
        - Total spending
        - Transaction count
        - Average transaction value
        - Top category
        - Last transaction date

        Args:
            df: Transaction DataFrame

        Returns:
            Customer aggregated DataFrame
        """
        logger.info("Aggregating customer metrics...")

        customer_metrics = df.groupby("customer_id").agg({
            "transaction_id": "count",
            "amount": ["sum", "mean", "std", "min", "max"],
            "category": lambda x: x.mode()[0] if len(x.mode()) > 0 else "Unknown",
            "transaction_date": ["min", "max"]
        }).reset_index()

        # Flatten column names
        customer_metrics.columns = [
            "customer_id",
            "transaction_count",
            "total_spending",
            "avg_transaction_value",
            "std_transaction_value",
            "min_transaction_value",
            "max_transaction_value",
            "top_category",
            "first_transaction_date",
            "last_transaction_date"
        ]

        # Fill NaN std with 0
        customer_metrics["std_transaction_value"] = customer_metrics["std_transaction_value"].fillna(0)

        logger.info(f"Customer metrics shape: {customer_metrics.shape}")

        return customer_metrics

    def aggregate_category_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate metrics by category by month.

        Args:
            df: Transaction DataFrame

        Returns:
            Category aggregated DataFrame
        """
        logger.info("Aggregating category metrics...")

        df["year_month"] = df["transaction_date"].dt.to_period("M")

        category_metrics = df.groupby(["year_month", "category"]).agg({
            "transaction_id": "count",
            "amount": ["sum", "mean"]
        }).reset_index()

        category_metrics.columns = [
            "year_month",
            "category",
            "transaction_count",
            "total_volume",
            "avg_transaction_value"
        ]

        logger.info(f"Category metrics shape: {category_metrics.shape}")

        return category_metrics

    def transform(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Full transformation pipeline.

        Args:
            df: Raw transaction DataFrame

        Returns:
            Tuple of (cleaned_transactions, customer_metrics, category_metrics)
        """
        logger.info("="*60)
        logger.info("STARTING TRANSFORMATION PIPELINE")
        logger.info("="*60)

        # Clean
        cleaned_df = self.clean_transactions(df)

        # Enrich
        enriched_df = self.enrich_transactions(cleaned_df)

        # Aggregate
        customer_metrics = self.aggregate_customer_metrics(enriched_df)
        category_metrics = self.aggregate_category_metrics(enriched_df)

        logger.info("="*60)
        logger.info("TRANSFORMATION PIPELINE COMPLETED")
        logger.info("="*60)

        return enriched_df, customer_metrics, category_metrics


# Example usage
if __name__ == "__main__":
    # Import ingestion module
    from ingestion import FinancialDataIngestion

    # Ingest data
    ingestion = FinancialDataIngestion("../data")
    raw_df = ingestion.ingest(source="mock", n_transactions=100000)

    # Transform data
    transformer = FinancialDataTransformer()
    transactions, customers, categories = transformer.transform(raw_df)

    print("\n✅ Transactions shape:", transactions.shape)
    print("✅ Customers shape:", customers.shape)
    print("✅ Categories shape:", categories.shape)
