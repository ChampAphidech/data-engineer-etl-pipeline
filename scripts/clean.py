# ==============================
# Import Library
# ==============================

# ใช้ pandas สำหรับจัดการข้อมูลตาราง (DataFrame)
import pandas as pd


# ==============================
# Clean Data Function
# ==============================

def clean_data(**context):
    # ดึง TaskInstance (ti) จาก Airflow context
    # ใช้สำหรับรับ-ส่งข้อมูลผ่าน XCom
    ti = context['ti']

    # ==============================
    # Load Data from XCom
    # ==============================

    # ดึงข้อมูล trades ที่ถูก extract มาแล้ว (อยู่ในรูป JSON)
    # แล้วแปลงกลับเป็น pandas DataFrame
    trades = pd.read_json(ti.xcom_pull(key='trades'))


    # ==============================
    # Clean String Columns
    # ==============================

    # แปลงค่า side (BUY/SELL) ให้เป็นตัวพิมพ์ใหญ่ และตัด space
    trades['side'] = trades['side'].str.upper().str.strip()

    # แปลง status ให้เป็นรูปแบบเดียวกัน (เช่น EXECUTED)
    trades['status'] = trades['status'].str.upper().str.strip()


    # ==============================
    # Convert Data Types
    # ==============================

    # แปลง quantity เป็นตัวเลข
    # errors='coerce' → ถ้าแปลงไม่ได้จะกลายเป็น NaN
    trades['quantity'] = pd.to_numeric(trades['quantity'], errors='coerce')

    # แปลง price เป็นตัวเลข
    trades['price'] = pd.to_numeric(trades['price'], errors='coerce')

    # แปลง fees เป็นตัวเลข
    trades['fees'] = pd.to_numeric(trades['fees'], errors='coerce')


    # ==============================
    # Handle Missing Values
    # ==============================

    # ลบ row ที่ไม่มี client_id หรือ instrument_id
    # เพราะถือว่าเป็นข้อมูลสำคัญ (key fields)
    trades = trades.dropna(subset=['client_id', 'instrument_id'])


    # ==============================
    # Push Clean Data to XCom
    # ==============================

    # แปลง DataFrame กลับเป็น JSON
    # แล้วส่งต่อให้ task ถัดไป (validate)
    ti.xcom_push(key='trades_clean', value=trades.to_json())