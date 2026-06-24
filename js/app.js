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
const pages = [document.getElementById('page-0'), document.getElementById('page-1'), document.getElementById('page-2')];
const tabs = document.querySelectorAll('.tab-btn');

function switchTab(targetIndex) {
    pages.forEach((page, idx) => page.classList.toggle('hidden', idx !== targetIndex));
    tabs.forEach((tab, idx) => tab.classList.toggle('active', idx === targetIndex));
    
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
// 6. ระบบวาดกราฟเส้นสถิติด้วย Native Canvas API
// ==========================================
function drawChart() {
    const canvas = document.getElementById('gradeChart');
    if (!canvas || !canvas.getContext) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.offsetWidth;
    const height = canvas.height = 240;
    
    // 💡 คลังข้อมูลเกรดตัวแปร (เดี๋ยวเขียนเชื่อม Fetch API ดึงค่าจาก Python มาเสียบตรงนี้)
    const grades = [3.20, 3.40, 3.10, 3.50, 3.42];
    const labels = ['ม.4 เทอม 1', 'ม.4 เทอม 2', 'ม.5 เทอม 1', 'ม.5 เทอม 2', 'ปัจจุบัน'];
    
    const padding = 50;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    
    ctx.clearRect(0, 0, width, height);
    
    // วาดเส้นแกนกราฟตารางหลังบ้าน
    ctx.strokeStyle = '#334155'; 
    ctx.lineWidth = 1;
    ctx.beginPath(); 
    ctx.moveTo(padding, padding); 
    ctx.lineTo(padding, height - padding); 
    ctx.lineTo(width - padding, height - padding); 
    ctx.stroke();
    
    const stepX = chartWidth / (grades.length - 1);
    
    // วาดโครงเส้นกราฟพัฒนาการ (Line Chart)
    ctx.strokeStyle = '#f59e0b'; 
    ctx.lineWidth = 3; 
    ctx.beginPath();
    
    grades.forEach((grade, i) => {
        const x = padding + i * stepX;
        // ลอจิกแปลงเกรด (ช่วง 2.0 - 4.0) ให้ออกมาเป็นพิกัดความสูงบนหน้าจอ Canvas Y
        const y = height - padding - ((grade - 2) / 2) * chartHeight;
        
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();
    
    // พ่นข้อความทศนิยมตัวเลขเกรดและจุดพิกัดวงกลมสีทอง
    grades.forEach((grade, i) => {
        const x = padding + i * stepX;
        const y = height - padding - ((grade - 2) / 2) * chartHeight;
        
        // ถมฟอนต์ตัวอักษรกำกับแกน X และจุดเกรด
        ctx.fillStyle = '#94a3b8'; 
        ctx.font = '500 11px Libre Franklin';
        ctx.textAlign = 'center';
        
        // พ่นข้อความหัวข้อเทอมด้านล่างแกน
        ctx.fillText(labels[i], x, height - 15);
        // พ่นตัวเลขเกรดลอยเหนือจุดวงกลม
        ctx.fillStyle = '#ffffff';
        ctx.fillText(grade.toFixed(2), x, y - 14);
        
        // เจาะพิกัดพ่นจุดวงกลมสีส้มทอง
        ctx.beginPath(); 
        ctx.arc(x, y, 5, 0, Math.PI * 2); 
        ctx.fillStyle = '#f59e0b'; 
        ctx.fill();
        
        // วาดขอบวงกลมสีขาวล้อมรอบจุดอีกชั้นเพิ่มความหรู
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.stroke();
    });
}

// โหลดกราฟครั้งแรกและผูกสัญญาระบบเมื่อมีการขยายหน้าจอเบราว์เซอร์ (Responsive redraw)
setTimeout(drawChart, 150);
window.addEventListener('resize', drawChart);
