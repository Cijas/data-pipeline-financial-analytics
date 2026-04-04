-- =====================================================
-- Financial Analytics SQL Queries
-- =====================================================
-- These queries demonstrate analytics on the processed data
-- In production, these would run on a data warehouse (Snowflake, BigQuery, etc.)

-- ===========================================
-- 1. TOP CUSTOMERS BY SPENDING
-- ===========================================
-- Identifies high-value customers and their contribution to revenue

SELECT 
    customer_id,
    transaction_count,
    total_spending,
    avg_transaction_value,
    ROUND((total_spending / SUM(total_spending) OVER()) * 100, 2) as revenue_share_pct,
    top_category,
    last_transaction_date
FROM customer_metrics
ORDER BY total_spending DESC
LIMIT 20;


-- ===========================================
-- 2. SPENDING DISTRIBUTION BY CATEGORY
-- ===========================================
-- Shows revenue breakdown by spending category

SELECT 
    category,
    SUM(total_volume) as total_volume,
    AVG(avg_transaction_value) as avg_transaction_value,
    SUM(transaction_count) as total_transactions,
    ROUND(SUM(total_volume) / SUM(SUM(total_volume)) OVER() * 100, 2) as category_share_pct
FROM category_metrics
GROUP BY category
ORDER BY total_volume DESC;


-- ===========================================
-- 3. MONTHLY TREND ANALYSIS
-- ===========================================
-- Tracks spending trends over time

SELECT 
    year_month,
    SUM(total_volume) as monthly_spending,
    COUNT(DISTINCT customer_id) as active_customers,
    AVG(avg_transaction_value) as avg_transaction_value,
    SUM(transaction_count) as total_transactions
FROM category_metrics
GROUP BY year_month
ORDER BY year_month DESC;


-- ===========================================
-- 4. CUSTOMER SEGMENTATION
-- ===========================================
-- Segments customers by spending patterns

SELECT 
    CASE 
        WHEN total_spending >= 10000 THEN 'VIP'
        WHEN total_spending >= 5000 THEN 'Premium'
        WHEN total_spending >= 1000 THEN 'Standard'
        ELSE 'New' 
    END as customer_segment,
    COUNT(customer_id) as segment_count,
    ROUND(AVG(total_spending), 2) as avg_spending,
    ROUND(AVG(transaction_count), 2) as avg_transactions,
    ROUND(AVG(avg_transaction_value), 2) as avg_transaction_value
FROM customer_metrics
GROUP BY 
    CASE 
        WHEN total_spending >= 10000 THEN 'VIP'
        WHEN total_spending >= 5000 THEN 'Premium'
        WHEN total_spending >= 1000 THEN 'Standard'
        ELSE 'New' 
    END
ORDER BY avg_spending DESC;


-- ===========================================
-- 5. CATEGORY PREFERENCE BY SEGMENT
-- ===========================================
-- Shows preferred categories by customer segment

WITH customer_segments AS (
    SELECT 
        customer_id,
        CASE 
            WHEN total_spending >= 10000 THEN 'VIP'
            WHEN total_spending >= 5000 THEN 'Premium'
            WHEN total_spending >= 1000 THEN 'Standard'
            ELSE 'New' 
        END as segment
    FROM customer_metrics
)
SELECT 
    cs.segment,
    category,
    COUNT(*) as transactions,
    ROUND(SUM(total_volume), 2) as total_volume
FROM category_metrics cm
GROUP BY cs.segment, category
ORDER BY cs.segment, total_volume DESC;


-- ===========================================
-- 6. GROWTH METRICS
-- ===========================================
-- Month-on-month growth analysis

WITH monthly_data AS (
    SELECT 
        year_month,
        SUM(total_volume) as spending
    FROM category_metrics
    GROUP BY year_month
)
SELECT 
    year_month,
    spending,
    LAG(spending) OVER (ORDER BY year_month) as prev_month_spending,
    ROUND(
        (spending - LAG(spending) OVER (ORDER BY year_month)) / 
        LAG(spending) OVER (ORDER BY year_month) * 100, 
        2
    ) as mom_growth_pct
FROM monthly_data
ORDER BY year_month;


-- ===========================================
-- 7. HIGH-VALUE CUSTOMER ANALYSIS
-- ===========================================
-- Deep dive into top 5% of customers

SELECT 
    customer_id,
    total_spending,
    transaction_count,
    avg_transaction_value,
    max_transaction_value,
    first_transaction_date,
    last_transaction_date,
    DATEDIFF(day, first_transaction_date, last_transaction_date) as days_active,
    top_category
FROM customer_metrics
WHERE total_spending >= (
    SELECT PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY total_spending)
    FROM customer_metrics
)
ORDER BY total_spending DESC;


-- ===========================================
-- 8. TRANSACTION VELOCITY
-- ===========================================
-- Customers with increasing transaction frequency

WITH customer_metrics_monthly AS (
    SELECT 
        customer_id,
        EXTRACT(YEAR_MONTH FROM transaction_date) as year_month,
        COUNT(*) as monthly_transactions
    FROM transactions
    GROUP BY customer_id, EXTRACT(YEAR_MONTH FROM transaction_date)
)
SELECT 
    customer_id,
    COUNT(*) as months_active,
    MIN(monthly_transactions) as min_monthly_transactions,
    MAX(monthly_transactions) as max_monthly_transactions,
    ROUND(AVG(monthly_transactions), 2) as avg_monthly_transactions
FROM customer_metrics_monthly
GROUP BY customer_id
HAVING COUNT(*) > 3
ORDER BY max_monthly_transactions DESC
LIMIT 20;
