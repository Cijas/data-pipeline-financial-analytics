"""
Financial Data Pipeline Package
=================================

A production-ready data pipeline for financial transaction analysis.

Modules:
    - ingestion: Data loading from CSV/API
    - transformation: Data cleaning, enrichment, aggregation
    - pipeline: Main orchestrator

Author: Lucas Cijas
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Lucas Cijas"
__description__ = "End-to-end data pipeline for financial analytics"

from .ingestion import FinancialDataIngestion
from .transformation import FinancialDataTransformer
from .pipeline import FinancialPipeline

__all__ = [
    "FinancialDataIngestion",
    "FinancialDataTransformer",
    "FinancialPipeline"
]
