# ==============================
# Import Libraries
# ==============================

# ใช้สำหรับสร้าง DAG (workflow)
from airflow import DAG

# ใช้สำหรับสร้าง task ที่รัน Python function
from airflow.operators.python import PythonOperator

# ใช้กำหนดวันเริ่มต้นของ DAG
from datetime import datetime

# ใช้จัดการ path เพื่อให้ import module ภายนอกได้
import sys


# ==============================
# Fix Python Path
# ==============================

# เพิ่ม path /opt/airflow เพื่อให้ Python หา folder scripts เจอ
# (สำคัญมากใน Docker environment)
sys.path.append('/opt/airflow')


# ==============================
# Import ETL Functions
# ==============================

# import function จากแต่ละ step ของ ETL pipeline
# extract → อ่านข้อมูล
# clean → ทำความสะอาด
# validate → ตรวจสอบความถูกต้อง
# load → โหลดเข้า database

from scripts.extract import extract_data
from scripts.clean import clean_data
from scripts.validate import validate_data
from scripts.load import load_data


# ==============================
# Default Arguments
# ==============================

# กำหนดค่า default ให้ DAG
default_args = {
    'owner': 'airflow',  # เจ้าของ DAG
    'start_date': datetime(2026, 3, 1),  # วันเริ่มต้น (Airflow ต้องมี)
}


# ==============================
# Define DAG
# ==============================

# สร้าง DAG ชื่อ etl_pipeline
with DAG(
    dag_id='etl_pipeline',        # ชื่อ DAG ที่จะแสดงใน UI
    default_args=default_args,    # ใช้ config ด้านบน
    schedule_interval="0 */3 * * *", # ทดสอบตั้ง schedule ให้ run ทุกๆ 3 ชั่วโมง หรือสามารถ run manual ได้
    catchup=False                # ไม่ย้อนรันย้อนหลัง
) as dag:

    # ==============================
    # Task 1: Extract
    # ==============================

    # อ่านข้อมูลจาก CSV
    t1 = PythonOperator(
        task_id='extract',              # ชื่อ task
        python_callable=extract_data    # function ที่จะรัน
    )


    # ==============================
    # Task 2: Clean
    # ==============================

    # ทำความสะอาดข้อมูล เช่น trim, convert type
    t2 = PythonOperator(
        task_id='clean',
        python_callable=clean_data
    )


    # ==============================
    # Task 3: Validate
    # ==============================

    # ตรวจสอบข้อมูล เช่น foreign key, business rule
    t3 = PythonOperator(
        task_id='validate',
        python_callable=validate_data
    )


    # ==============================
    # Task 4: Load
    # ==============================

    # โหลดข้อมูลเข้า PostgreSQL
    t4 = PythonOperator(
        task_id='load',
        python_callable=load_data
    )


    # ==============================
    # Define Task Order (Pipeline Flow)
    # ==============================

    # กำหนดลำดับการทำงานของ pipeline
    # extract → clean → validate → load
    t1 >> t2 >> t3 >> t4