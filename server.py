from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import os

app = FastAPI()

# Mount โฟลเดอร์ CSS และ js ให้หน้าเว็บเรียกใช้ได้ปกติ
app.mount("/CSS", StaticFiles(directory="CSS"), name="CSS")
app.mount("/js", StaticFiles(directory="js"), name="js")

DB_FILE = "students.db"

# ฟังก์ชันสร้างฐานข้อมูลจำลอง (จะรันเฉพาะตอนที่ยังไม่มีไฟล์ students.db)
def init_mock_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # สร้าง Table สำหรับเก็บข้อมูลนักเรียน
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                student_id TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # ยัดข้อมูลนักเรียนจำลอง (มึงสามารถเพิ่มชื่อเพื่อน ชื่อคนอื่น หรือพี่คนนั้นได้ตรงนี้เลย 555+)
        mock_data = [
            ("สมชาย", "สายโค้ด", "12345", "benjama2026"),
            ("สมหญิง", "รักเรียน", "54321", "pass1234"),
            ("มูฮัมหมัด", "ซัดหมด", "99999", "admin999")
        ]
        
        cursor.executemany('''
            INSERT INTO students (firstname, lastname, student_id, password) 
            VALUES (?, ?, ?, ?)
        ''', mock_data)
        
        conn.commit()
        conn.close()
        print("💡 [Database] สร้างฐานข้อมูลจำลองสำเร็จเรียบร้อยแล้วมึง!")

# รันระบบสร้างฐานข้อมูลทันทีที่เปิดเซิร์ฟเวอร์
init_mock_db()

# 1. หน้าแรกพ่นหน้าจอ Login ดักไว้
@app.get("/", response_class=HTMLResponse)
def get_login():
    with open("login.html", "r", encoding="utf-8") as f:
        return f.read()

# 2. ตัวรับแรงกระแทก ตรวจสอบข้อมูลจากหน้า Login ชนิดที่ว่า "ต้องตรงกันหมดทุกฟิลด์"
@app.post("/login")
def handle_login(
    firstname: str = Form(...), 
    lastname: str = Form(...), 
    username: str = Form(...), # ฟิลด์เลขประจำตัวนักเรียนใน HTML ของมึงตั้ง name="username" ไว้
    password: str = Form(...)
):
    # เชื่อมต่อ Database ไปตรวจเช็กค่า
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # คำสั่ง SQL เช็กเข้ม: ชื่อตรง นามสกุลตรง รหัสตรง พาสเวิร์ดตรง!
    cursor.execute('''
        SELECT * FROM students 
        WHERE firstname = ? AND lastname = ? AND student_id = ? AND password = ?
    ''', (firstname.strip(), lastname.strip(), username.strip(), password.strip()))
    
    user = cursor.fetchone()
    conn.close()

    if user:
        # ถ้าเจอข้อมูลในฐานข้อมูล (ข้อมูลถูกต้องครบถ้วน) -> ปล่อยผ่านไปหน้า Portal
        return RedirectResponse(url="/portal", status_code=303)
    else:
        # ถ้าฟิลด์ใดฟิลด์หนึ่งไม่ตรง หรือไม่มีในฐานข้อมูล -> ถีบหัวส่งกลับไปหน้าเอ๋อ (หรือมึงจะแต่งหน้านี้เพิ่มทีหลังได้)
        return HTMLResponse(
            content="""
            <div style='background-color: #0f172a; color: #f43f5e; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: sans-serif;'>
                <h1 style='font-size: 2rem;'>❌ ข้อมูลไม่ถูกต้อง</h1>
                <p style='color: #94a3b8; margin-top: 10px;'>ชื่อ นามสกุล รหัสนักเรียน หรือรหัสผ่าน ไม่ตรงกับฐานข้อมูลจำลองเลย</p>
                <a href='/' style='margin-top: 20px; color: #fbbf24; text-decoration: none; font-weight: bold;'>กลับไปลองใหม่ดิ๊</a>
            </div>
            """, 
            status_code=401
        )

# 3. หน้าแดนสวรรค์ Portal (เข้าได้เมื่อล็อกอินผ่าน)
@app.get("/portal", response_class=HTMLResponse)
def get_portal():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
