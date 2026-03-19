# Data Dictionary

## Overview

This document describes the schema, definitions, and data quality rules for the dataset produced by the ETL pipeline.

---

## Table: fact_trades

This table contains cleaned and validated trade transaction data used for analytics and reporting.

---

## Columns

| Column Name   | Data Type | Nullable | Description                                               | Example             |
| ------------- | --------- | -------- | --------------------------------------------------------- | ------------------- |
| trade_id      | TEXT      | No       | Unique identifier for each trade                          | T0001               |
| trade_time    | TIMESTAMP | No       | Timestamp when the trade was executed                     | 2026-03-09 10:00:00 |
| client_id     | TEXT      | No       | Identifier of the client executing the trade              | C001                |
| instrument_id | TEXT      | No       | Identifier of the traded instrument                       | I001                |
| side          | TEXT      | No       | Trade direction (BUY or SELL)                             | BUY                 |
| quantity      | INTEGER   | No       | Number of units traded (must be greater than 0)           | 10                  |
| price         | FLOAT     | No       | Price per unit of the instrument (must be greater than 0) | 185.25              |
| fees          | FLOAT     | Yes      | Transaction fee associated with the trade                 | 1.25                |
| status        | TEXT      | No       | Trade status (only EXECUTED is retained)                  | EXECUTED            |

---

## Data Quality Rules

The following validation rules are applied in the ETL pipeline:

* Records must have valid `client_id` and `instrument_id`
* `client_id` must exist in the clients dataset
* `instrument_id` must exist in the instruments dataset
* `quantity` must be greater than 0
* `price` must be greater than 0
* Only records with `status = 'EXECUTED'` are loaded
* Invalid or missing key fields are removed during cleaning

---

## Data Source

* clients.csv (client master data)
* instruments.csv (instrument reference data)
* trades_YYYY-MM-DD.csv (daily transaction data)

---

## Data Flow

```text
Extract → Clean → Validate → Load → fact_trades
```

---

## Assumptions

* Input files follow a consistent schema
* Trade data is delivered daily
* Duplicate handling is not implemented in the current version

---

## Future Improvements

* Implement deduplication (e.g., primary key or upsert)
* Store intermediate data outside XCom for scalability
* Add dimension tables (clients, instruments)
* Add monitoring and alerting for pipeline failures

---
