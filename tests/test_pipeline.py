"""
Unit tests for the Financial Data Pipeline

Tests cover:
- Data ingestion
- Data transformation
- Pipeline orchestration
- Data quality checks
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ingestion import FinancialDataIngestion
from transformation import FinancialDataTransformer
from pipeline import FinancialPipeline


class TestIngestion:
    """Tests for data ingestion module."""
    
    @pytest.fixture
    def ingestion(self, tmp_path):
        """Create ingestion instance with temporary directory."""
        return FinancialDataIngestion(str(tmp_path))
    
    def test_mock_data_generation(self, ingestion):
        """Test mock transaction generation."""
        df = ingestion.generate_mock_transactions(n_transactions=1000)
        
        assert len(df) == 1000
        assert "transaction_id" in df.columns
        assert "customer_id" in df.columns
        assert "amount" in df.columns
        assert df["amount"].min() >= 0
    
    def test_raw_data_save(self, ingestion):
        """Test saving raw data."""
        df = ingestion.generate_mock_transactions(n_transactions=100)
        path = ingestion.save_raw_data(df)
        
        assert Path(path).exists()
        saved_df = pd.read_csv(path)
        assert len(saved_df) == 100


class TestTransformation:
    """Tests for data transformation module."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample transaction data."""
        return pd.DataFrame({
            "transaction_id": ["TXN_001", "TXN_002", "TXN_003"],
            "customer_id": ["CUST_001", "CUST_002", "CUST_001"],
            "transaction_date": pd.date_range("2024-01-01", periods=3),
            "amount": [100.0, -50.0, 200.0],
            "category": ["Food", "Food", "Shopping"],
            "merchant": ["Merchant_001", "Merchant_002", "Merchant_001"],
            "status": ["completed", "failed", "completed"]
        })
    
    def test_data_cleaning(self, sample_data):
        """Test data cleaning removes negative amounts."""
        transformer = FinancialDataTransformer()
        cleaned = transformer.clean_transactions(sample_data)
        
        assert len(cleaned) == 2  # Negative amount removed
        assert (cleaned["amount"] > 0).all()
    
    def test_enrichment(self, sample_data):
        """Test data enrichment adds temporal features."""
        transformer = FinancialDataTransformer()
        cleaned = transformer.clean_transactions(sample_data)
        enriched = transformer.enrich_transactions(cleaned)
        
        assert "transaction_month" in enriched.columns
        assert "transaction_year" in enriched.columns
        assert "is_weekend" in enriched.columns
    
    def test_customer_aggregation(self, sample_data):
        """Test customer metric aggregation."""
        transformer = FinancialDataTransformer()
        cleaned = transformer.clean_transactions(sample_data)
        enriched = transformer.enrich_transactions(cleaned)
        customers = transformer.aggregate_customer_metrics(enriched)
        
        assert len(customers) == 2  # Two unique customers
        assert "total_spending" in customers.columns
        assert "transaction_count" in customers.columns


class TestPipeline:
    """Tests for pipeline orchestration."""
    
    @pytest.fixture
    def pipeline(self, tmp_path):
        """Create pipeline instance with temporary directory."""
        return FinancialPipeline(str(tmp_path))
    
    def test_pipeline_execution(self, pipeline):
        """Test complete pipeline execution."""
        results = pipeline.run(source="mock", n_transactions=1000)
        
        assert results["status"] == "success"
        assert "execution_time_seconds" in results
        assert results["execution_time_seconds"] > 0
    
    def test_output_files_created(self, pipeline):
        """Test that all output files are created."""
        results = pipeline.run(source="mock", n_transactions=1000)
        
        for file_type, path in results["output_files"].items():
            assert Path(path).exists(), f"Missing output file: {file_type}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
