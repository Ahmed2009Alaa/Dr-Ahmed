from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
app.secret_key = 'super_secret_key'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

DB_PATH = 'alameed.db'

def get_db():
    return sqlite3.connect(DB_PATH)

# ✅ الصفحة الرئيسية (تسجيل الدخول)
@app.route('/')
def login_page():
    return render_template('login.html')

# ✅ معالجة تسجيل الدخول
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == '1234' and password == '1234':
        session['user'] = 'teacher'
        return redirect(url_for('teacher_page'))

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        session['user'] = username
        session['grade'] = user[3]
        return redirect(url_for('student_page'))
    else:
        return render_template('login.html', message="❌ اسم المستخدم أو كلمة السر غير صحيح")

# ✅ صفحة المعلم
@app.route('/teacher')
def teacher_page():
    if session.get('user') != 'teacher':
        return redirect(url_for('login_page'))
    return render_template('teacher.html')

# ✅ صفحة الطالب
@app.route('/student')
def student_page():
    if not session.get('user') or session.get('user') == 'teacher':
        return redirect(url_for('login_page'))
    return render_template('student.html')

# ✅ رفع درس
@app.route('/upload_lecture', methods=['POST'])
def upload_lecture():
    title = request.form['title']
    grade = request.form['grade']
    file = request.files['video']

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO lectures (title, filename, grade) VALUES (?, ?, ?)", (title, filename, grade))
        conn.commit()
        conn.close()
        return jsonify({'message': '✅ تم رفع المحاضرة بنجاح'})
    else:
        return jsonify({'message': '❌ لم يتم رفع أي ملف'}), 400

# ✅ عرض المحاضرات
@app.route('/get_lectures')
def get_lectures():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, title, filename, grade FROM lectures ORDER BY id DESC")
    lectures = [{'id': row[0], 'title': row[1], 'filename': row[2], 'grade': row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify({'lectures': lectures})

# ✅ حذف محاضرة
@app.route('/delete_lecture', methods=['POST'])
def delete_lecture():
    data = request.get_json()
    lecture_id = data.get('id')

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT filename FROM lectures WHERE id=?", (lecture_id,))
    result = c.fetchone()

    if result:
        filename = result[0]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        c.execute("DELETE FROM lectures WHERE id=?", (lecture_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': '🗑️ تم حذف المحاضرة'})
    else:
        return jsonify({'message': '❌ لم يتم العثور على المحاضرة'}), 404
# ✅ رفع امتحان
@app.route('/upload_exam', methods=['POST'])
def upload_exam():
    title = request.form['title']
    grade = request.form['grade']
    file = request.files['exam']

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO exams (title, filename, grade) VALUES (?, ?, ?)", (title, filename, grade))
        conn.commit()
        conn.close()

        return jsonify({'message': '✅ تم رفع الامتحان بنجاح'})
    else:
        return jsonify({'message': '❌ لم يتم رفع أي ملف'}), 400
# ✅ عرض الامتحانات
@app.route('/get_exams')
def get_exams():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, title, filename, grade FROM exams ORDER BY id DESC")
    exams = [{'id': row[0], 'title': row[1], 'filename': row[2], 'grade': row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify({'exams': exams})

# ✅ إضافة طالب
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    grade = data.get('grade')

    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, grade) VALUES (?, ?, ?)", (username, password, grade))
        conn.commit()
        msg = '✅ تم إضافة الطالب بنجاح'
    except sqlite3.IntegrityError:
        msg = '⚠️ اسم المستخدم موجود بالفعل'
    finally:
        conn.close()

    return jsonify({'message': msg})

# ✅ إرسال ملاحظة للطالب (اختياري - placeholder)
@app.route('/send_note', methods=['POST'])
def send_note():
    # يمكن تنفيذه لاحقًا وربطه بقاعدة بيانات للملاحظات
    return jsonify({'message': '📩 تم إرسال الملاحظة (تجريبي)'})

# ✅ تقديم الفيديوهات
@app.route('/uploads/<path:filename>')
def serve_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ✅ تشغيل السيرفر
if __name__ == '__main__':
    app.run(debug=True)
