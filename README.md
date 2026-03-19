# Data Engineer Take Home

## Architecture

This project implements an end-to-end ETL pipeline using:

* **Airflow** for orchestration
* **PostgreSQL** as the target database
* **Docker Compose** for reproducible environment setup

Pipeline flow:

```
Extract → Clean → Validate → Load
```

---

## How to Run

Start all services:

```bash
docker-compose up --build
```

---

## Initialize Airflow (First Time Only)

```bash
docker exec -it de_airflow bash

export AIRFLOW_HOME=/opt/airflow

airflow db init

airflow users create \
  --username admin \
  --password admin \
  --firstname admin \
  --lastname user \
  --role Admin \
  --email admin@test.com
```

---

## Access Airflow

* URL: http://localhost:8080
* Username: admin
* Password: admin

---

## Trigger Pipeline

* Enable DAG: `etl_pipeline`
* Click **Trigger DAG**

---

## Output

The pipeline loads cleaned and validated data into:

```
fact_trades
```

---

## Data Dictionary
See docs/data_dictionary.md

---

## Example Queries

```sql
SELECT COUNT(*) FROM fact_trades;

SELECT * FROM fact_trades LIMIT 10;
```

---

## Data Processing Logic

### Cleaning

* Standardize string fields (upper + trim)
* Convert numeric fields safely
* Remove records with missing key fields

### Validation

* Ensure valid `client_id` and `instrument_id`
* Filter invalid business records:

  * quantity <= 0
  * price <= 0
  * non-EXECUTED trades

---

## Design Decisions

* **Pandas**: simple and effective for CSV transformation
* **Airflow**: orchestration and task dependency management
* **Docker**: ensures reproducibility for reviewers
* **XCom**: used for passing small datasets between tasks

---

## Limitations / Future Improvements

* No deduplication (pipeline is not fully idempotent)
* XCom is not suitable for large-scale data
* Dimension tables (clients, instruments) are not persisted
* No retry or alerting mechanism implemented

---

## Notes

This solution focuses on clarity, correctness, and reproducibility while keeping the implementation simple and practical.
