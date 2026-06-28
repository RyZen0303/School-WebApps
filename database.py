import sqlite3
import os

DB_FILE = "students.db"

def init_mock_db():
    # ลบ DB เก่าทิ้งก่อนถ้ามี เพื่อให้ข้อมูลอัปเดตตัวล่าสุดสดๆ ใหม่ๆ
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. สร้างตารางข้อมูลส่วนตัวนักเรียน
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
    
    # 2. สร้างตารางเก็บเกรดรายเทอม (สำหรับไปดึงทำกราฟหน้าบ้าน)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            term TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            credit REAL NOT NULL,
            grade REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    ''')
    
    # 3. ยัดข้อมูลจำลองชุดใหญ่ (Mock Data แหล่งรวมรายชื่อเด็ก)
    mock_students = [
        ("สมชาย", "สายโค้ด", "12345", "benjama2026", "01/01/2552"),
        ("สมหญิง", "รักเรียน", "54321", "pass1234", "14/02/2551"),
        ("มูฮัมหมัด", "ซัดหมด", "99999", "admin999", "27/06/2552")
    ]
    cursor.executemany('''
        INSERT INTO students (firstname, lastname, student_id, password, birthdate) 
        VALUES (?, ?, ?, ?, ?)
    ''', mock_students)
    
    # 4. ยัดข้อมูลเกรดจำลองของเด็กๆ แยกรายเทอม (ตัวนี้แหละที่จะเอาไปคำนวณทำกราฟ GPA)
    mock_grades = [
        # --- เกรดของ สมชาย (รหัส 12345) ค่อยๆ ไต่ระดับเรียนดีขึ้น ---
        ("12345", "ม.4-1", "คณิตศาสตร์", 1.5, 3.0),
        ("12345", "ม.4-1", "วิทยาศาสตร์", 1.5, 3.5),
        ("12345", "ม.4-1", "ภาษาอังกฤษ", 1.0, 2.5), # เฉลี่ย ม.4-1 = 3.12
        
        ("12345", "ม.4-2", "คณิตศาสตร์", 1.5, 3.5),
        ("12345", "ม.4-2", "วิทยาศาสตร์", 1.5, 3.5),
        ("12345", "ม.4-2", "ภาษาอังกฤษ", 1.0, 3.0), # เฉลี่ย ม.4-2 = 3.37
        
        ("12345", "ม.5-1", "คณิตศาสตร์", 1.5, 4.0),
        ("12345", "ม.5-1", "วิทยาศาสตร์", 1.5, 3.5),
        ("12345", "ม.5-1", "ภาษาอังกฤษ", 1.0, 4.0), # เฉลี่ย ม.5-1 = 3.81
        
        # --- เกรดของ สมหญิง (รหัส 54321) ตัวแม่เรียนเทพคงที่ ---
        ("54321", "ม.4-1", "คณิตศาสตร์", 1.5, 4.0),
        ("54321", "ม.4-1", "วิทยาศาสตร์", 1.5, 4.0),
        ("54321", "ม.4-1", "ภาษาอังกฤษ", 1.0, 3.5),
        
        ("54321", "ม.4-2", "คณิตศาสตร์", 1.5, 3.5),
        ("54321", "ม.4-2", "วิทยาศาสตร์", 1.5, 4.0),
        ("54321", "ม.4-2", "ภาษาอังกฤษ", 1.0, 4.0),
        
        ("54321", "ม.5-1", "คณิตศาสตร์", 1.5, 4.0),
        ("54321", "ม.5-1", "วิทยาศาสตร์", 1.5, 4.0),
        ("54321", "ม.5-1", "ภาษาอังกฤษ", 1.0, 4.0),

        # 💡 [ยัดเพิ่มตรงนี้มึง] --- เกรดของ มูฮัมหมัด (รหัส 99999) โหดจัด ม.1 กับ ม.6 โดดๆ ตามที่มึงวางโครงไว้ ---
        ("99999", "ม.1-1", "คณิตศาสตร์", 1.5, 3.0),
        ("99999", "ม.1-1", "วิทยาศาสตร์", 1.5, 4.0),
        ("99999", "ม.1-1", "ภาษาอังกฤษ", 1.0, 3.5), # เฉลี่ย ม.1-1 = 3.50
        
        ("99999", "ม.6-1", "คณิตศาสตร์", 1.5, 4.0),
        ("99999", "ม.6-1", "วิทยาศาสตร์", 1.5, 3.5),
        ("99999", "ม.6-1", "ภาษาอังกฤษ", 1.0, 4.0), # เฉลี่ย ม.6-1 = 3.81
    ]
    cursor.executemany('''
        INSERT INTO student_grades (student_id, term, subject_name, credit, grade) 
        VALUES (?, ?, ?, ?, ?)
    ''', mock_grades)
    
    conn.commit()
    conn.close()
    print("💡 [Database] เสกตารางข้อมูลนักเรียนและเกรดรายเทอมเข้า SQLite สำเร็จแล้วมึง!")

# อัลกอริทึมสำหรับคำนวณหาเกรดเฉลี่ย (GPA) แยกตามเทอมของนักเรียนแต่ละคน
def get_student_gpa_by_term(student_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # ไปดึงเกรดและหน่วยกิตทั้งหมดของเด็กคนนี้มา
    cursor.execute('''
        SELECT term, credit, grade FROM student_grades 
        WHERE student_id = ?
    ''', (student_id,))
    rows = cursor.fetchall()
    conn.close()
    
    # สร้างดิกชันนารีเก็บประวัติคำนวณ: { "ม.4-1": [หน่วยกิตรวม, ผลรวมของเกรด*หน่วยกิต] }
    term_data = {}
    for term, credit, grade in rows:
        if term not in term_data:
            term_data[term] = {"total_credit": 0.0, "weighted_sum": 0.0}
        term_data[term]["total_credit"] += credit
        term_data[term]["weighted_sum"] += (credit * grade)
        
    # คำนวณหา GPA สุทธิของแต่ละเทอม: สูตรคือ (ผลรวมของเกรด*หน่วยกิต) / หน่วยกิตรวม
    gpa_by_term = {}
    for term, data in term_data.items():
        if data["total_credit"] > 0:
            gpa_by_term[term] = round(data["weighted_sum"] / data["total_credit"], 2)
            
    return gpa_by_term # ส่งคืนค่าเป็น เช่น {"ม.4-1": 3.12, "ม.4-2": 3.37, ...}

if __name__ == "__main__":
    init_mock_db()