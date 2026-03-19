# ==============================
# Import Library
# ==============================

# ใช้ pandas สำหรับจัดการข้อมูลแบบตาราง
import pandas as pd


# ==============================
# Validate Data Function
# ==============================

def validate_data(**context):
    # ดึง TaskInstance (ti) จาก Airflow context
    # ใช้สำหรับรับ-ส่งข้อมูลผ่าน XCom
    ti = context['ti']

    # ==============================
    # Load Data from XCom
    # ==============================

    # โหลดข้อมูล trades ที่ผ่านการ clean แล้ว
    trades = pd.read_json(ti.xcom_pull(key='trades_clean'))

    # โหลด master data ของ clients
    clients = pd.read_json(ti.xcom_pull(key='clients'))

    # โหลด master data ของ instruments
    instruments = pd.read_json(ti.xcom_pull(key='instruments'))


    # ==============================
    # Validate Reference Integrity
    # ==============================

    # ดึง list ของ client_id ที่ valid จาก master table
    valid_clients = clients['client_id'].unique()

    # ดึง list ของ instrument_id ที่ valid จาก master table
    valid_instruments = instruments['instrument_id'].unique()

    # filter เฉพาะ trades ที่มี client และ instrument ถูกต้อง
    # (เหมือน foreign key validation)
    trades = trades[
        trades['client_id'].isin(valid_clients) &
        trades['instrument_id'].isin(valid_instruments)
    ]


    # ==============================
    # Apply Business Rules
    # ==============================

    # quantity ต้องมากกว่า 0
    trades = trades[trades['quantity'] > 0]

    # price ต้องมากกว่า 0
    trades = trades[trades['price'] > 0]

    # เอาเฉพาะ transaction ที่ status = EXECUTED
    trades = trades[trades['status'] == 'EXECUTED']


    # ==============================
    # Push Valid Data to XCom
    # ==============================

    # แปลง DataFrame เป็น JSON แล้วส่งต่อไป task ถัดไป (load)
    ti.xcom_push(key='trades_valid', value=trades.to_json())