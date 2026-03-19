# ==============================
# Import Library
# ==============================

# ใช้ pandas สำหรับอ่านและจัดการข้อมูล CSV
import pandas as pd


# ==============================
# Define Base Path
# ==============================

# path ของไฟล์ input ภายใน container
# (สำคัญ: ต้องใช้ absolute path ใน Docker environment)
BASE_PATH = "/opt/airflow/data/input"


# ==============================
# Extract Data Function
# ==============================

def extract_data(**context):
    # ==============================
    # Read CSV Files
    # ==============================

    # อ่านข้อมูลลูกค้า (master data)
    clients = pd.read_csv(f"{BASE_PATH}/clients.csv")

    # อ่านข้อมูล instruments (master data)
    instruments = pd.read_csv(f"{BASE_PATH}/instruments.csv")

    # อ่านข้อมูล trades (transaction data)
    trades = pd.read_csv(f"{BASE_PATH}/trades_2026-03-09.csv")


    # ==============================
    # Push Data to XCom
    # ==============================

    # ใช้ XCom ส่งข้อมูลไปยัง task ถัดไป
    # แปลง DataFrame → JSON (เพราะ XCom รองรับข้อมูลขนาดเล็ก)
    
    context['ti'].xcom_push(
        key='clients',
        value=clients.to_json()
    )

    context['ti'].xcom_push(
        key='instruments',
        value=instruments.to_json()
    )

    context['ti'].xcom_push(
        key='trades',
        value=trades.to_json()
    )