from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import os
# 🔗 ดึงฟังก์ชันคำนวณ GPA เทพๆ จากไฟล์ database.py มาใช้งาน
from database import get_student_gpa_by_term 

app = FastAPI()

app.mount("/CSS", StaticFiles(directory="CSS"), name="CSS")
app.mount("/js", StaticFiles(directory="js"), name="js")

DB_FILE = "students.db"

# ❌ ลบฟังก์ชัน init_mock_db() ตัวเก่าออกจากตรงนี้แล้ว เพราะมันย้ายไปทำงานหล่อๆ อยู่ที่ database.py แทน

@app.get("/", response_class=HTMLResponse)
def get_login():
    with open("login.html", "r", encoding="utf-8") as f:
        return f.read()

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
        response = RedirectResponse(url="/portal", status_code=303)
        response.set_cookie(key="current_student_id", value=username.strip(), httponly=True)
        return response
    else:
        return HTMLResponse(content="<h1 style='color:red; text-align:center; margin-top:50px;'>❌ ข้อมูลด่านแรกไม่ถูกต้อง!</h1>", status_code=401)

@app.get("/portal", response_class=HTMLResponse)
def get_portal():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/grade-auth", response_class=HTMLResponse)
def get_grade_auth():
    with open("grade-auth.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/grade-auth/verify")
def verify_grade_auth(
    request: Request,
    student_id: str = Form(...),
    birthdate: str = Form(...)
):
    logged_in_id = request.cookies.get("current_student_id")
    
    if not logged_in_id or logged_in_id != student_id.strip():
        return HTMLResponse(
            content="""
            <div style='background-color: #0f172a; color: #f43f5e; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: sans-serif;'>
                <h1>❌ ตรวจพบการสวมรอยระบบ!</h1>
                <p style='color: #94a3b8; margin-top: 10px;'>รหัสนักเรียนไม่ตรงกับบัญชีที่กำลังใช้งานอยู่ในปัจจุบันมึง!</p>
                <a href='/portal' style='margin-top: 20px; color: #fbbf24; text-decoration: none;'>กลับหน้าหลัก</a>
            </div>
            """, status_code=403
        )
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE student_id = ? AND birthdate = ?', (student_id.strip(), birthdate.strip()))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return RedirectResponse(url="/grades-view", status_code=303)
    else:
        return HTMLResponse(content="<h1 style='color:red; text-align:center; margin-top:50px;'>❌ วันเกิดไม่ถูกต้องสำหรับรหัสประจำตัวนี้!</h1>", status_code=401)

@app.get("/grades-view", response_class=HTMLResponse)
def get_grades_view():
    with open("grades-view.html", "r", encoding="utf-8") as f:
        return f.read()

# 🎯 [เพิ่มใหม่] เส้น API สำหรับส่งเกรดเฉลี่ยรายเทอมไปดึงวาดกราฟใน index.html
@app.get("/api/student-gpa")
def get_gpa_data(request: Request):
    student_id = request.cookies.get("current_student_id")
    if not student_id:
        return {"error": "Unauthorized"}, 401
        
    # เรียกฟังก์ชันคำนวณเกรดที่อยู่ข้ามไฟล์ (ใน database.py) ออกมาใช้งานได้เลย
    gpa_dict = get_student_gpa_by_term(student_id)
    return gpa_dict