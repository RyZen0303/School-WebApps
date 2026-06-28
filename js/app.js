// ==========================================
// 1. ระบบวันเวลาและการเปิดระบบไอคอนเริ่มต้น
// ==========================================
const now = new Date();
document.getElementById('current-date').textContent = now.toLocaleDateString('th-TH', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
});

// รันระบบไอคอน Lucide ให้แสดงผลทับ HTML
lucide.createIcons();

// ==========================================
// 2. ระบบสลับหน้าแท็บเมนูแบบไร้รอยต่อ (Tab Switching)
// ==========================================

function switchTab(targetIndex) {
    // 💡 ย้ายการดึงค่ามาไว้ "ในฟังก์ชัน" เพื่อให้มันวิ่งไปจับปุ่ม HTML สดๆ ทุกครั้งที่กดคลิก
    const currentPages = [document.getElementById('page-0'), document.getElementById('page-1'), document.getElementById('page-2')];
    const currentTabs = document.querySelectorAll('.tab-btn');

    // ลอจิกสลับซ่อน/แสดงหน้าเพจ
    currentPages.forEach((page, idx) => {
        if (page) page.classList.toggle('hidden', idx !== targetIndex);
    });
    
    // ลอจิกสลับคลาส active เพื่อให้เส้นใต้สีส้มของมึงทำงาน
    currentTabs.forEach((tab, idx) => {
        tab.classList.toggle('active', idx === targetIndex);
    });
    
    // ถ้าสลับมาที่แดชบอร์ด (หน้า 3) ให้วาดกราฟใหม่เพื่อให้ขนาดสเกลตรงกับหน้าจอคอมปัจจุบัน
    if (targetIndex === 2) {
        setTimeout(drawChart, 50);
    }
}

// ==========================================
// 3. ระบบคำนวณเกรดจำลอง (GPA Calculator)
// ==========================================
function addGpaRow() {
    const container = document.getElementById('gpa-inputs');
    const row = document.createElement('div');
    row.className = 'flex gap-2';
    row.innerHTML = `
        <input type="number" placeholder="หน่วยกิต" class="w-1/2 px-3 py-2 rounded bg-slate-700 text-white text-sm border border-slate-600 focus:outline-none focus:border-amber-400 font-medium" min="1" max="6">
        <input type="number" placeholder="เกรด (0-4)" class="w-1/2 px-3 py-2 rounded bg-slate-700 text-white text-sm border border-slate-600 focus:outline-none focus:border-amber-400 font-medium" min="0" max="4" step="0.5">
    `;
    container.appendChild(row);
}

function calcGpa() {
    const rows = document.getElementById('gpa-inputs').children;
    let totalCredits = 0, totalPoints = 0;
    
    for (const row of rows) {
        const inputs = row.querySelectorAll('input');
        const credits = parseFloat(inputs[0].value) || 0;
        const grade = parseFloat(inputs[1].value) || 0;
        
        totalCredits += credits; 
        totalPoints += credits * grade;
    }
    
    const gpa = totalCredits > 0 ? (totalPoints / totalCredits).toFixed(2) : '0.00';
    document.getElementById('gpa-result').textContent = 'GPA: ' + gpa;
}

// ==========================================
// 4. ระบบนาฬิกาจับเวลาดิจิทัล (Timer Mechanism)
// ==========================================
let timerInterval = null, timerSeconds = 0;

function updateTimerDisplay() {
    const h = String(Math.floor(timerSeconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((timerSeconds % 3600) / 60)).padStart(2, '0');
    const s = String(timerSeconds % 60).padStart(2, '0');
    document.getElementById('timer-display').textContent = `${h}:${m}:${s}`;
}

function startTimer() { 
    if (!timerInterval) {
        timerInterval = setInterval(() => { 
            timerSeconds++; 
            updateTimerDisplay(); 
        }, 1000); 
    } 
}

function stopTimer() { 
    clearInterval(timerInterval); 
    timerInterval = null; 
}

function resetTimer() { 
    stopTimer(); 
    timerSeconds = 0; 
    updateTimerDisplay(); 
}

// ==========================================
// 5. ระบบมินิแบบทดสอบจำลอง (Quiz Engine)
// ==========================================
const quizData = [
    { q: 'ฐานข้อมูลโมเดลการเสิร์ชที่ดึงค่าข้อมูลตรงเป้าในครั้งเดียวทันที มีค่า Time Complexity เท่าใด?', choices: ['O(n)', 'O(log n)', 'O(1)', 'O(n^2)'], answer: 2 },
    { q: 'Library ของ Python ตัวใดที่ใช้สแกนและแกะข้อมูลข้อความออกจากไฟล์ PDF ได้เฉียบที่สุด?', choices: ['pandas', 'pdfplumber', 'Tkinter', 'Math'], answer: 1 },
    { q: 'CSS Framework ตัวใดที่คุณสมบัติคลาสเปิดทางให้ดีไซน์หน้าเว็บจบได้ในแท็ก HTML โดยตรง?', choices: ['Bootstrap', 'Bulma', 'Tailwind CSS', 'Sass'], answer: 2 }
];

let currentQuizIndex = 0;

function renderQuiz() {
    const currentQuiz = quizData[currentQuizIndex];
    document.getElementById('quiz-question').textContent = `${currentQuizIndex + 1}. ${currentQuiz.q}`;
    document.getElementById('quiz-feedback').textContent = '';
    
    const choicesContainer = document.getElementById('quiz-choices');
    choicesContainer.innerHTML = '';
    
    currentQuiz.choices.forEach((choice, index) => {
        const button = document.createElement('button');
        button.className = 'choice-btn w-full text-left px-4 py-2.5 rounded text-sm bg-slate-700 text-slate-200 border border-slate-600 font-medium';
        button.textContent = choice;
        button.onclick = () => checkAnswer(index, button);
        choicesContainer.appendChild(button);
    });
}

function checkAnswer(selectedIndex, clickedButton) {
    const choiceButtons = document.getElementById('quiz-choices').children;
    for (const btn of choiceButtons) btn.disabled = true;
    
    const correctAnswerIndex = quizData[currentQuizIndex].answer;
    const feedbackElement = document.getElementById('quiz-feedback');
    
    if (selectedIndex === correctAnswerIndex) {
        clickedButton.classList.add('correct');
        feedbackElement.textContent = '✓ ถูกต้อง!';
        feedbackElement.style.color = '#4ade80';
    } else {
        clickedButton.classList.add('wrong');
        choiceButtons[correctAnswerIndex].classList.add('correct');
        feedbackElement.textContent = '✗ ผิด!';
        feedbackElement.style.color = '#f87171';
    }
    
    // ตั้งเวลาดีเลย์ 1.8 วินาทีเพื่อสไลด์เปลี่ยนข้อถัดไป
    setTimeout(() => { 
        currentQuizIndex = (currentQuizIndex + 1) % quizData.length; 
        renderQuiz(); 
    }, 1800);
}

renderQuiz();

// ==========================================
// 6. ระบบวาดกราฟเส้นสถิติด้วย Native Canvas API (เวอร์ชัน Dynamic ดึงจาก Python หลังบ้าน)
// ==========================================
async function drawChart() {
    const canvas = document.getElementById('gradeChart');
    if (!canvas || !canvas.getContext) return;
    
    const ctx = canvas.getContext('2d');
    
    try {
        // 🚀 1. ยิง Fetch API ไปดึงข้อมูลเกรดคำนวณสดๆ จาก Python (FastAPI) 
        const response = await fetch('/api/student-gpa');
        if (!response.ok) throw new Error('ไม่สามารถดึงข้อมูลเกรดจากหลังบ้านได้มึง');
        const gpaData = await response.json();

        console.log("📊 ข้อมูลเกรดที่ดึงมาได้จากหลังบ้าน:", gpaData);
        
        // ดักกรณีถ้าไม่มีข้อมูลเกรด หรือยังไม่ได้ล็อกอิน ให้เคลียร์จอแล้วหยุดทำงาน
        if (!gpaData || Object.keys(gpaData).length === 0) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            return;
        }

        // 2. แกะข้อมูล Object ผูกดิกชันนารี {"เทอม": เกรด} ออกมาเป็น Array
        const labels = Object.keys(gpaData);   // ดึงชื่อเทอมไปทำแกน X -> ['ม.4-1', 'ม.4-2', 'ม.5-1']
        const grades = Object.values(gpaData); // ดึงตัวเลขเกรดไปทำแกน Y -> [3.12, 3.37, 3.81]

        // 🔥 [ของแถมโอเวอร์คิล] คำนวณหาค่าเฉลี่ยสะสม (GPAX) จริงของเด็กคนนี้ แล้วพ่นลงการ์ดสรุปผลหน้าบ้าน
        const sumGpa = grades.reduce((total, val) => total + val, 0);
        const gpaxResult = (sumGpa / grades.length).toFixed(2);
        const gpaxCard = document.getElementById('gpax-display');
        if (gpaxCard) gpaxCard.textContent = gpaxResult;

        // 3. กำหนดขนาดพื้นที่วาดภาพ Canvas
        const width = canvas.width = canvas.offsetWidth;
        const height = canvas.height = 240;
        const padding = 50;
        const chartWidth = width - padding * 2;
        const chartHeight = height - padding * 2;
        
        ctx.clearRect(0, 0, width, height);
        
        // วาดเส้นแกนกราฟตารางพื้นหลัง
        ctx.strokeStyle = '#334155'; 
        ctx.lineWidth = 1;
        ctx.beginPath(); 
        ctx.moveTo(padding, padding); 
        ctx.lineTo(padding, height - padding); 
        ctx.lineTo(width - padding, height - padding); 
        ctx.stroke();
        
        // คำนวณระยะห่างระหว่างจุดแกน X (ดักบั๊กเผื่อเด็กมีข้อมูลเทอมเดียว)
        const stepX = grades.length > 1 ? chartWidth / (grades.length - 1) : chartWidth;
        
        // 4. เริ่มวาดโครงเส้นกราฟพัฒนาการ (Line Chart)
        ctx.strokeStyle = '#f59e0b'; 
        ctx.lineWidth = 3; 
        ctx.beginPath();
        
        grades.forEach((grade, i) => {
            const x = padding + i * stepX;
            // ลอจิกแปลงเกรด (ช่วง 2.0 - 4.0) ให้สัมพันธ์กับความสูงแนวตั้งแกน Y ของจอ Canvas
            const y = height - padding - ((grade - 2) / 2) * chartHeight;
            
            if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        });
        ctx.stroke();
        
        // 5. ถมฟอนต์ข้อความตัวอักษรเกรดกำกับและจุดพิกัดวงกลมสีทอง
        grades.forEach((grade, i) => {
            const x = padding + i * stepX;
            const y = height - padding - ((grade - 2) / 2) * chartHeight;
            
            ctx.fillStyle = '#94a3b8'; 
            ctx.font = '500 11px Libre Franklin';
            ctx.textAlign = 'center';
            
            // พ่นข้อความชื่อภาคเรียนด้านล่าง
            ctx.fillText(labels[i], x, height - 15);
            // พ่นตัวเลขเกรดจริงลอยเหนือหัวจุดวงกลม
            ctx.fillStyle = '#ffffff';
            ctx.fillText(grade.toFixed(2), x, y - 14);
            
            // เจาะพ่นวงกลมสีส้มทองประกายขาวครอบ
            ctx.beginPath(); 
            ctx.arc(x, y, 5, 0, Math.PI * 2); 
            ctx.fillStyle = '#f59e0b'; 
            ctx.fill();
            
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1.5;
            ctx.stroke();
        });
    } catch (error) {
        console.error('❌ [Frontend Error] โหลดข้อมูลมาวาดกราฟไม่ผ่านมึง:', error);
    }
}

// โหลดกราฟครั้งแรกและผูกสัญญาระบบเมื่อมีการขยายหน้าจอเบราว์เซอร์ (Responsive redraw)
setTimeout(drawChart, 150);
window.addEventListener('resize', drawChart);