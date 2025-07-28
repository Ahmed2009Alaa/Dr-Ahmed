# create_database.py

import sqlite3

# إنشاء الاتصال بقاعدة البيانات
conn = sqlite3.connect('alameed.db')
c = conn.cursor()

# ✅ جدول الطلاب
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    grade INTEGER NOT NULL
)
''')

# ✅ جدول المحاضرات
c.execute('''
CREATE TABLE IF NOT EXISTS lectures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    filename TEXT NOT NULL,
    grade INTEGER NOT NULL
)
''')

# ✅ جدول الامتحانات
c.execute('''
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    filename TEXT NOT NULL,
    grade INTEGER NOT NULL
)
''')

# ✅ جدول الملاحظات
c.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    to_user TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# حفظ وإنهاء الاتصال
conn.commit()
conn.close()

print("✅ تم إنشاء قاعدة البيانات alameed.db بكل الجداول بنجاح")
