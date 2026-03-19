# ==============================
# Import Libraries
# ==============================

# ใช้ pandas สำหรับจัดการข้อมูล DataFrame
import pandas as pd

# ใช้ SQLAlchemy สำหรับเชื่อมต่อฐานข้อมูล
from sqlalchemy import create_engine


# ==============================
# Database Connection String
# ==============================

# connection string สำหรับเชื่อม PostgreSQL
# format: postgresql+driver://user:password@host:port/database
DB_CONN = "postgresql+psycopg2://de_user:de_pass@postgres:5432/brokerage"


# ==============================
# Load Data Function
# ==============================

def load_data(**context):
    # ดึง TaskInstance จาก Airflow context
    # ใช้สำหรับดึงข้อมูลจาก XCom
    ti = context['ti']

    # ==============================
    # Load Data from XCom
    # ==============================

    # ดึงข้อมูล trades ที่ผ่าน validate แล้ว
    # และแปลงจาก JSON → DataFrame
    trades = pd.read_json(ti.xcom_pull(key='trades_valid'))


    # ==============================
    # Create Database Connection
    # ==============================

    # สร้าง engine สำหรับเชื่อมต่อ PostgreSQL
    engine = create_engine(DB_CONN)


    # ==============================
    # Load Data into Database
    # ==============================

    # บันทึกข้อมูลลง table 'fact_trades'
    # if_exists='append' → เพิ่มข้อมูลใหม่เข้าไป (ไม่ลบทิ้ง)
    # index=False → ไม่เอา index ของ pandas ลง DB
    trades.to_sql(
        name='fact_trades',
        con=engine,
        if_exists='append',
        index=False
    )