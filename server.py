from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import os

app = FastAPI()

# Mount โฟลเดอร์ CSS และ js
app.mount("/CSS", StaticFiles(directory="CSS"), name="CSS")
app.mount("/js", StaticFiles(directory="js"), name="js")

DB_FILE = "students.db"

def init_mock_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                student_id TEXT NOT NULL,
                password TEXT NOT NULL,
                birthdate TEXT NOT NULL
            )
        ''')
        mock_data = [
            ("สมชาย", "สายโค้ด", "12345", "benjama2026", "01/01/2552"),
            ("สมหญิง", "รักเรียน", "54321", "pass1234", "14/02/2551"),
            ("มูฮัมหมัด", "ซัดหมด", "99999", "admin999", "27/06/2552")
        ]
        cursor.executemany('''
            INSERT INTO students (firstname, lastname, student_id, password, birthdate) 
            VALUES (?, ?, ?, ?, ?)
        ''', mock_data)
        conn.commit()
        conn.close()
        print("💡 [Database] สร้างฐานข้อมูลจำลองพร้อมคอลัมน์ วันเกิด สำเร็จแล้วมึง!")

init_mock_db()

@app.get("/", response_class=HTMLResponse)
def get_login():
    with open("login.html", "r", encoding="utf-8") as f:
        return f.read()

# 🔐 ด่านแรก: ล็อกอินผ่าน -> แจกคุกกี้จำรหัสนักเรียนไว้
@app.post("/login")
def handle_login(
    firstname: str = Form(...), 
    lastname: str = Form(...), 
    username: str = Form(...), 
    password: str = Form(...)
):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM students 
        WHERE firstname = ? AND lastname = ? AND student_id = ? AND password = ?
    ''', (firstname.strip(), lastname.strip(), username.strip(), password.strip()))
    
    user = cursor.fetchone()
    conn.close()

    if user:
        # ยินดีด้วยมึงผ่านด่านแรก! สร้างแอปเด้งไปหน้าหน้าพอร์ทัลพร้อมฝัง Cookie ยืนยันตัวตน
        response = RedirectResponse(url="/portal", status_code=303)
        response.set_cookie(key="current_student_id", value=username.strip(), httponly=True)
        return response
    else:
        return HTMLResponse(content="<h1 style='color:red; text-align:center; margin-top:50px;'>❌ ข้อมูลด่านแรกไม่ถูกต้อง!</h1>", status_code=401)

@app.get("/portal", response_class=HTMLResponse)
def get_portal():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# 🎫 ด่านสอง: เรียกหน้าต่างล็อกอินเช็กเกรด (รหัสนักเรียน + วันเกิด)
@app.get("/grade-auth", response_class=HTMLResponse)
def get_grade_auth():
    with open("grade-auth.html", "r", encoding="utf-8") as f:
        return f.read()

# 🔍 ตัวประมวลผลด่านสอง: ตรวจสอบความถูกต้องของเซสชัน
@app.post("/grade-auth/verify")
def verify_grade_auth(
    request: Request,
    student_id: str = Form(...),
    birthdate: str = Form(...)
):
    # 1. ดึงคุกกี้ที่บันทึกไว้ตอนล็อกอินหน้าแรกมาตรวจสอบ
    logged_in_id = request.cookies.get("current_student_id")
    
    # ถ้าไม่มีคุกกี้ หรือรหัสนักเรียนที่พิมพ์มาดันไม่ตรงกับคนที่ล็อกอินเข้าระบบไว้ตอนแรก
    if not logged_in_id or logged_in_id != student_id.strip():
        return HTMLResponse(
            content="""
            <div style='background-color: #0f172a; color: #f43f5e; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: sans-serif;'>
                <h1 style='font-size: 2rem;'>❌ ตรวจพบการสวมรอยระบบ!</h1>
                <p style='color: #94a3b8; margin-top: 10px;'>รหัสนักเรียนไม่ตรงกับบัญชีที่กำลังใช้งานอยู่ในปัจจุบันมึง!</p>
                <a href='/portal' style='margin-top: 20px; color: #fbbf24; text-decoration: none;'>กลับหน้าหลัก</a>
            </div>
            """, status_code=403
        )
        
    # 2. ถ้ารหัสนักเรียนตรงกันจริง ไปดักเช็กวันเกิดใน DB ต่อ
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE student_id = ? AND birthdate = ?', (student_id.strip(), birthdate.strip()))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        # ผ่านสองด่านแบบโอเวอร์คิล! วาร์ปส่งตัวไปหน้าดูเกรดตัวจริง
        return RedirectResponse(url="/grades-view", status_code=303)
    else:
        return HTMLResponse(content="<h1 style='color:red; text-align:center; margin-top:50px;'>❌ วันเกิดไม่ถูกต้องสำหรับรหัสประจำตัวนี้!</h1>", status_code=401)

# 🏆 หน้าใบเกรดมหาเทพตัวจริง (เมื่อผ่านครบทุกเงื่อนไข)
@app.get("/grades-view", response_class=HTMLResponse)
def get_grades_view():
    with open("grades-view.html", "r", encoding="utf-8") as f:
        return f.read()