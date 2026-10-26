# Databricks notebook source
# DBTITLE 1,TASK 8 - WHY HAS THE MARGIN MOVED?
# MAGIC %sql
# MAGIC WITH SALES AS (
# MAGIC     SELECT
# MAGIC     p.product_line,
# MAGIC     YEAR(o.order_date) AS year,
# MAGIC     l.line_revenue AS revenue,
# MAGIC     l.line_revenue - l.cogs AS profit
# MAGIC
# MAGIC     FROM sizwe_sales_orders o
# MAGIC     JOIN sizwe_sales_lines l
# MAGIC     ON o.order_id = l.order_id
# MAGIC     JOIN sizwe_products p
# MAGIC     ON l.sku = p.sku
# MAGIC     WHERE o.order_date >= '2024-01-01'
# MAGIC     AND o.order_date < '2026-01-01'
# MAGIC )
# MAGIC SELECT
# MAGIC     product_line,
# MAGIC     SUM( CASE WHEN year = 2024 THEN 
# MAGIC     revenue ELSE 0 END) AS revenue_2024,
# MAGIC     SUM( CASE WHEN year = 2025 THEN 
# MAGIC     revenue ELSE 0 END) AS revenue_2025,
# MAGIC     ROUND(100.0 * SUM(CASE WHEN year = 2024 THEN profit ELSE 0 END)
# MAGIC     / NULLIF(SUM(CASE WHEN year = 2024 THEN revenue ELSE 0 END), 0), 2)
# MAGIC     AS margin_2024,
# MAGIC     ROUND(100.0 * SUM(CASE WHEN year = 2025 THEN profit ELSE 0 END)
# MAGIC     / NULLIF(SUM(CASE WHEN year = 2025 THEN revenue ELSE 0 END), 0), 2)
# MAGIC     AS margin_2025
# MAGIC     FROM SALES
# MAGIC     GROUP BY product_line
# MAGIC     ORDER BY product_line
# MAGIC
# MAGIC     
# MAGIC

# COMMAND ----------

#BASED ON THE REVENUE TOTALS I CALCULSTED, REVENUE FOR FY2025 DECREASED ACROSS ALL FIVE PORODUCT LINES, WHICH GO AGAIUNST THE GROWTH STATED IN THE TASK.


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_products

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_sales_orders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_sales_lines

# COMMAND ----------

# DBTITLE 1,TASK 7 -  THE SHAPE OF THE YEAR.
# MAGIC %sql
# MAGIC WITH monthly AS (
# MAGIC     SELECT date_trunc('month', so.order_date) AS month,
# MAGIC       SUM(sl.line_revenue) AS revenue
# MAGIC       FROM   sizwe_sales_orders so
# MAGIC     JOIN sizwe_sales_lines sl
# MAGIC       ON so.order_id = sl.order_id
# MAGIC       GROUP BY date_trunc('month', so.order_date)
# MAGIC )
# MAGIC SELECT
# MAGIC     month,
# MAGIC     revenue,
# MAGIC     (revenue / LAG(revenue, 1) OVER (ORDER BY month) - 1) * 100
# MAGIC         AS percentage_change,
# MAGIC     AVG(revenue) OVER (
# MAGIC         ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
# MAGIC         ) AS rolling_3_month_average
# MAGIC FROM monthly
# MAGIC ORDER BY MONTH
# MAGIC
# MAGIC
# MAGIC     

# COMMAND ----------

 #REVENUE DECLINES AT THE END OF THE YEAR.
 #SIZWE'S QUIETIEST MONTH IS DECEMBER, WITH A REVENUE OF 29 MILLION.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_sales_lines

# COMMAND ----------

# DBTITLE 1,TASK 6 - ARE THE SALES REPRESENTATIVES HITTING TARGETS?
# MAGIC %sql
# MAGIC SELECT
# MAGIC     r.rep_id,
# MAGIC     r.rep_name,
# MAGIC     r.territory,
# MAGIC     r.target_monthly,
# MAGIC     COALESCE(SUM(sl.line_revenue),0) /12.0
# MAGIC       / r.target_monthly * 100 AS percentage_of_target
# MAGIC       FROM   sizwe_reps r
# MAGIC     LEFT JOIN sizwe_sales_orders so
# MAGIC       ON r.rep_id = so.rep_id
# MAGIC     LEFT JOIN sizwe_sales_lines sl
# MAGIC       ON so.order_id = sl.order_id
# MAGIC       AND so.order_date >= '2025-01-01'
# MAGIC       AND so.order_date < '2026-01-01'
# MAGIC     GROUP BY
# MAGIC     r.rep_id,
# MAGIC     r.rep_name,
# MAGIC     r.territory,
# MAGIC     r.target_monthly
# MAGIC     ORDER BY percentage_of_target DESC;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_sales_lines

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_reps

# COMMAND ----------

# DBTITLE 1,TASK 5 - A COMMERCIAL GAP
# MAGIC %sql
# MAGIC SELECT
# MAGIC     C.trading_name,
# MAGIC     C.segment,
# MAGIC     C.province,
# MAGIC     SUM(SL.line_revenue) AS total_revenue
# MAGIC     FROM   sizwe_customers C
# MAGIC     JOIN sizwe_sales_orders so
# MAGIC     ON C.customer_id = so.customer_id
# MAGIC     JOIN sizwe_sales_lines sl
# MAGIC     ON so.order_id = sl.order_id
# MAGIC     WHERE LOWER(c.channel) = 'wholesale'
# MAGIC     AND NOT EXISTS (
# MAGIC         SELECT 1
# MAGIC         FROM sizwe_trade_promotions tp
# MAGIC         WHERE tp.promo_id = C.customer_id
# MAGIC     )
# MAGIC     GROUP BY 
# MAGIC     C.customer_id,
# MAGIC     C.trading_name,
# MAGIC     C.segment,
# MAGIC     C.province
# MAGIC     ORDER BY total_revenue DESC
# MAGIC     LIMIT (15);
# MAGIC
# MAGIC     
# MAGIC
# MAGIC

# COMMAND ----------

    #I'LL GIVE A DISCOUNT ON THE NEXT ORDER, FOR THE TOP THREE WHOLESALE CUSTOMERS TO REWARD THEIR HIGHTENED REVENUE CONTRIBUTION, STRENGTHEN BUSINESS RELATIONSHIPS AND EXPLORE FURTURE OPPORTUNITIES


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_sales_lines

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_sales_orders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_trade_promotions

# COMMAND ----------

# DBTITLE 1,TASK 4 - THE TEN ACCOUNTS THAN MATTER MOST
# MAGIC %sql
# MAGIC SELECT
# MAGIC     C.trading_name,
# MAGIC     C.segment,
# MAGIC     C.province,
# MAGIC     R.rep_name,
# MAGIC     C.rep_id,
# MAGIC     SUM(SL.line_revenue) AS revenue_2025
# MAGIC     FROM   sizwe_customers C
# MAGIC     JOIN sizwe_sales_orders so
# MAGIC     ON C.customer_id = so.customer_id
# MAGIC     JOIN sizwe_sales_lines sl
# MAGIC     ON so.order_id = sl.order_id
# MAGIC     LEFT JOIN sizwe_reps R
# MAGIC     ON C.rep_id = R.rep_id
# MAGIC     WHERE so.order_date >= '2025-01-01'
# MAGIC      AND so.order_date < '2026-01-01'
# MAGIC     GROUP BY 
# MAGIC     C.customer_id,
# MAGIC     C.trading_name,
# MAGIC     C.segment,
# MAGIC     C.province,
# MAGIC     R.rep_name,
# MAGIC     C.rep_id
# MAGIC     ORDER BY revenue_2025 DESC
# MAGIC     LIMIT 10;
# MAGIC     
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_reps

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_sales_orders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_sales_lines

# COMMAND ----------

# DBTITLE 1,TASK 3 - THE COLLECTIONS PROBLEM
# MAGIC %sql  
# MAGIC SELECT
# MAGIC     C.channel,
# MAGIC     COUNT(*) AS number_of_invoices,
# MAGIC     SUM(CASE
# MAGIC         WHEN a.amount_settled >=
# MAGIC         a.invoice_amount THEN 1 
# MAGIC         ELSE 0
# MAGIC         END) AS settled_invoices,
# MAGIC         SUM(CASE
# MAGIC         WHEN a.amount_settled <
# MAGIC         a.invoice_amount THEN 1 
# MAGIC         ELSE 0
# MAGIC         END) AS open_invoices,
# MAGIC         AVG(
# MAGIC             CASE
# MAGIC             WHEN a.settlement_date is 
# MAGIC         NOT NULL
# MAGIC             THEN
# MAGIC         DATEDIFF(a.settlement_date,
# MAGIC         a.invoice_date)
# MAGIC         END
# MAGIC         ) AS avg_days_to_settle,
# MAGIC         SUM(a.invoice_amount - a.amount_settled) AS
# MAGIC         total_outstanding
# MAGIC         FROM sizwe_ar_ledger AS a
# MAGIC         JOIN sizwe_customers AS C
# MAGIC         ON a.customer_id = C.customer_id
# MAGIC         GROUP BY C.channel
# MAGIC         ORDER BY C.channel;
# MAGIC
# MAGIC

# COMMAND ----------

# DUE TO THE HIGH NUMBER OF OPEN INVOICES ON WHOLESALE. IT HIGHLIGHTS A BIGGER COLLECTION PROBLEM THAN SUBSCRIPTION.
#I WOULD INVESTIGATE WHOLESALES FIRST DEU TO ITS SIGNIFICANTLY HIGH NUMBER OF OPEN INVOICES.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_sales_orders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_ar_ledger

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_ap_payments

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT*
# MAGIC FROM sizwe_ap_invoices

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES;
# MAGIC

# COMMAND ----------

# DBTITLE 1,TASK 2 - WHERE THE PROFIT ACTUALLY COMES FROM
# MAGIC %sql
# MAGIC SELECT
# MAGIC   p.product_line,
# MAGIC   SUM(L.line_revenue) AS revenue,
# MAGIC   SUM(L.cogs) AS cost_of_goods,
# MAGIC   SUM(L.line_revenue) - SUM(L.cogs) AS gross_profit,
# MAGIC   (SUM(L.line_revenue) - 
# MAGIC   SUM(L.cogs))
# MAGIC     /NULLIF(SUM(L.line_revenue), 0) *100
# MAGIC     AS gross_profit_margin_percentage
# MAGIC FROM sizwe_products AS p
# MAGIC JOIN sizwe_sales_lines AS l
# MAGIC ON p. sku = L.sku
# MAGIC GROUP BY p.product_line
# MAGIC ORDER BY gross_profit DESC
# MAGIC

# COMMAND ----------

# HOUSE BLENT EARNS THE HIGHEST GRPSS PROFIT, UNFORTUNATELY IT DOES NOT EARN THE HIGHEST MARGIN.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE sizwe_sales_lines

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE sizwe_products;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE products;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES;

# COMMAND ----------

# DBTITLE 1,TASK 1 - CHANNEL PERFORMANCE
# MAGIC %sql
# MAGIC SELECT 
# MAGIC   O.channel,
# MAGIC     SUM(CASE
# MAGIC     WHEN O.order_date <= '2024-06-30'
# MAGIC       THEN L.line_revenue
# MAGIC     ELSE 0
# MAGIC     END) AS FY_2024_revenue,
# MAGIC
# MAGIC     SUM(CASE
# MAGIC       WHEN O.order_date > '2024-06-30'
# MAGIC       THEN L.line_revenue
# MAGIC       ELSE 0
# MAGIC       END) AS FY_2025_revenue,
# MAGIC       (
# MAGIC         SUM (CASE
# MAGIC             WHEN O.order_date > '2024-06-30'
# MAGIC             THEN L.line_revenue
# MAGIC             ELSE 0
# MAGIC         END)
# MAGIC         -
# MAGIC         SUM(CASE
# MAGIC             WHEN O.order_date <= '2024-06-30'
# MAGIC             THEN L.line_revenue
# MAGIC             ELSE 0
# MAGIC         END)
# MAGIC       )
# MAGIC       /
# MAGIC       NULLIF(
# MAGIC         SUM(CASE
# MAGIC             WHEN O.order_date <= '2024-06-30'
# MAGIC             THEN L.line_revenue
# MAGIC             ELSE 0
# MAGIC         END),
# MAGIC         0
# MAGIC        ) * 100 AS growth_rate_percent
# MAGIC     
# MAGIC FROM sizwe_sales_orders AS O
# MAGIC   JOIN sizwe_sales_lines AS L
# MAGIC   ON O.order_id = L.order_id
# MAGIC GROUP BY O.channel
# MAGIC ORDER BY O.channel;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC O.order_id,
# MAGIC O.order_date,
# MAGIC O.channel,
# MAGIC L.line_revenue
# MAGIC FROM sizwe_sales_orders AS O
# MAGIC JOIN sizwe_sales_lines AS L
# MAGIC ON O.order_id = L.order_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT channel
# MAGIC FROM sizwe_sales_orders;
# MAGIC