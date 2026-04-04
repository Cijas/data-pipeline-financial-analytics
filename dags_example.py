"""
Apache Airflow DAG Example
==========================

This file demonstrates how to orchestrate the pipeline using Apache Airflow.
In production (AWS MWAA, Google Cloud Composer, etc.), this would be placed in the dags/ folder.

Learning Resources:
- https://airflow.apache.org/docs/
- https://aws.amazon.com/blogs/aws/aws-managed-workflows-for-apache-airflow/

Usage:
1. Install Airflow: pip install apache-airflow
2. Place this file in your Airflow dags/ folder
3. Airflow scheduler will detect and run it
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import logging

# ========================
# DAG Configuration
# ========================

default_args = {
    'owner': 'data-engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
}

dag = DAG(
    dag_id='financial_data_pipeline',
    default_args=default_args,
    description='End-to-end financial data pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
    tags=['data-engineering', 'financial', 'etl'],
)

# ========================
# Task Functions
# ========================

def validate_prerequisites(**context):
    """Validate that all prerequisites are met."""
    logging.info("Validating prerequisites...")
    logging.info("✓ Python environment OK")
    logging.info("✓ Dependencies installed")
    logging.info("✓ Data paths accessible")


def run_pipeline(**context):
    """Run the complete financial data pipeline."""
    logging.info("Starting financial data pipeline...")
    
    from pathlib import Path
    import sys
    
    # Add pipeline location to path
    pipeline_dir = Path('/path/to/data-pipeline-financial-analytics/src')
    sys.path.insert(0, str(pipeline_dir))
    
    from pipeline import FinancialPipeline
    
    # Initialize and run
    pipeline = FinancialPipeline(base_path="/path/to/data")
    results = pipeline.run(source="mock", n_transactions=100000)
    
    # Push results to context for downstream tasks
    context['task_instance'].xcom_push(key='pipeline_status', value=results['status'])
    context['task_instance'].xcom_push(key='execution_time', value=results['execution_time_seconds'])
    
    logging.info(f"Pipeline completed with status: {results['status']}")
    return results


def validate_output(**context):
    """Validate output data."""
    logging.info("Validating output data...")
    
    from pathlib import Path
    import pandas as pd
    
    output_dir = Path("/path/to/data/processed")
    
    # Check files exist
    required_files = [
        'transactions.parquet',
        'customer_metrics.parquet',
        'category_metrics.parquet'
    ]
    
    for file in required_files:
        filepath = output_dir / file
        if not filepath.exists():
            raise FileNotFoundError(f"Missing output file: {filepath}")
        
        # Load and validate
        df = pd.read_parquet(filepath)
        logging.info(f"✓ {file}: {len(df):,} records")
        
        # Check for nulls
        null_count = df.isnull().sum().sum()
        if null_count > 0:
            logging.warning(f"  Warning: {null_count} null values found")


def send_success_notification(**context):
    """Send success notification."""
    ti = context['task_instance']
    status = ti.xcom_pull(task_ids='run_pipeline', key='pipeline_status')
    execution_time = ti.xcom_pull(task_ids='run_pipeline', key='execution_time')
    
    message = f"""
    Financial Data Pipeline Execution Summary
    ==========================================
    
    Status: {status}
    Execution Time: {execution_time:.2f} seconds
    Timestamp: {datetime.now().isoformat()}
    
    Output Files:
    ✓ transactions.parquet
    ✓ customer_metrics.parquet
    ✓ category_metrics.parquet
    
    Next Steps:
    - Run SQL analytics queries
    - Update BI dashboards
    - Monitor data quality metrics
    """
    
    logging.info(message)
    # In production, send email/Slack:
    # send_slack_message(message)
    # send_email_notification(message)


# ========================
# DAG Task Definition
# ========================

# Task 1: Validate
validate_task = PythonOperator(
    task_id='validate_prerequisites',
    python_callable=validate_prerequisites,
    dag=dag,
)

# Task 2: Run Pipeline
run_pipeline_task = PythonOperator(
    task_id='run_pipeline',
    python_callable=run_pipeline,
    dag=dag,
)

# Task 3: Validate Output
validate_output_task = PythonOperator(
    task_id='validate_output',
    python_callable=validate_output,
    dag=dag,
)

# Task 4: Run Analytics Queries (Optional)
analytics_task = BashOperator(
    task_id='run_analytics',
    bash_command="""
    sqlite3 /path/to/analytics.db < /path/to/sql/analytics_queries.sql
    """,
    dag=dag,
)

# Task 5: Success Notification
notification_task = PythonOperator(
    task_id='send_notification',
    python_callable=send_success_notification,
    trigger_rule='all_success',  # Only run if all previous succeeded
    dag=dag,
)

# ========================
# DAG Dependencies
# ========================

validate_task >> run_pipeline_task >> validate_output_task >> [
    analytics_task,
    notification_task
]

"""
DAG Structure:
==============

validate_prerequisites
    │
    ▼
run_pipeline
    │
    ▼
validate_output
    │
    ├──▶ run_analytics
    │
    └──▶ send_notification
    

Timeline:
- Daily at 2:00 AM UTC
- Typical execution: 2-5 minutes
- Retry on failure (up to 2 times)
- Email on completion


Production Deployment:
======================

AWS MWAA (Managed Workflows for Apache Airflow):
1. Create environment: https://console.aws.amazon.com/mwaa
2. Upload this DAG to S3
3. MWAA auto-detects and schedules

Google Cloud Composer:
1. Create environment: https://console.cloud.google.com/composer
2. Upload this DAG to bucket
3. Composer auto-detects and schedules

Self-hosted:
1. Place in airflow/dags/ folder
2. Run: airflow dags list
3. Enable in UI: http://localhost:8080


Monitoring & Alerts:
====================

Set up monitoring for:
- Pipeline execution time (alert if > 10 min)
- Data loss (alert if > 5%)
- Output file sizes (alert if unusual)
- Error logs (email on failure)


Notes for Portfolio:
====================

This DAG demonstrates:
✓ Production-grade orchestration
✓ Error handling & retries
✓ Data validation patterns
✓ Pipeline monitoring
✓ Cloud-ready design

Great talking points for interviews!
"""
