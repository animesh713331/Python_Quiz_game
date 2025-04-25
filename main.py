import sqlite3
import csv
import os
import time
import random
from datetime import datetime

DB_NAME = 'quiz_app.db'

# Change this to match your local CSV file path
CSV_FILE_PATH = "C:\\quiz_csv.csv"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')
    # Questions
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct_option TEXT,
        category TEXT,
        difficulty TEXT
    )''')
    # Scores
    c.execute('''CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER,
        category TEXT,
        difficulty TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()


def import_questions_from_csv(csv_file_path):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question_data = (
                row['question'], row['option_a'], row['option_b'],
                row['option_c'], row['option_d'],
                row['correct_option'].strip().upper(), row['category'].strip(), row['difficulty'].strip().capitalize()
            )
            c.execute('''INSERT INTO questions (
                question, option_a, option_b, option_c, option_d,
                correct_option, category, difficulty
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', question_data)
    conn.commit()
    conn.close()


def register():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    username = input("Enter username: ")
    password = input("Enter password (warning: not hidden): ")
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("✅ Registration successful!")
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")
    conn.close()


def login():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    username = input("Enter username: ")
    password = input("Enter password (warning: not hidden): ")
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        print("✅ Login successful!")
        return user[0]
    else:
        print("❌ Invalid credentials.")
        return None


def take_quiz(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    category = input("Enter category (or leave blank for any): ").strip()
    difficulty = input("Enter difficulty (Easy/Medium/Hard): ").strip().capitalize()

    query = "SELECT * FROM questions WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)
    c.execute(query, tuple(params))
    questions = c.fetchall()

    if not questions:
        print("❌ No questions found for the given filters.")
        return

    selected_questions = random.sample(questions, min(5, len(questions)))

    print(f"\n📦 Starting quiz with {len(selected_questions)} questions.")

    score = 0
    for q in selected_questions:
        print("\n" + q[1])
        print("A.", q[2])
        print("B.", q[3])
        print("C.", q[4])
        print("D.", q[5])
        start = time.time()
        answer = input("Answer (A/B/C/D): ").strip().upper()
        if time.time() - start > 15:
            print("⏰ Time's up!")
            continue
        if answer == q[6]:
            score += 1
            print("✅ Correct!")
        else:
            print(f"❌ Wrong! Correct was {q[6]}")

    print(f"\n🎯 Your Score: {score}/{len(selected_questions)}")
    c.execute("INSERT INTO scores (user_id, score, category, difficulty) VALUES (?, ?, ?, ?)",
              (user_id, score, category, difficulty))
    conn.commit()
    conn.close()


def view_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''SELECT users.username, scores.score, scores.category, scores.difficulty, scores.timestamp
                 FROM scores
                 JOIN users ON scores.user_id = users.id
                 ORDER BY score DESC, timestamp ASC
                 LIMIT 10''')
    rows = c.fetchall()
    print("\n🏆 Leaderboard:")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row[0]} - {row[1]} points ({row[2]}, {row[3]}) on {row[4]}")
    conn.close()


def menu():
    init_db()
    if not os.path.exists("questions_imported.flag"):
        import_questions_from_csv(CSV_FILE_PATH)
        open("questions_imported.flag", "w").close()
        print("✅ Initial questions imported.")

    while True:
        print("\n1. Register\n2. Login\n3. View Leaderboard\n4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
            if user_id:
                take_quiz(user_id)
        elif choice == '3':
            view_leaderboard()
        elif choice == '4':
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    menu()
