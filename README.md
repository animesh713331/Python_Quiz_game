![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)


# 🧠 Console-Based Python Quiz App with SQLite

A feature-rich console-based quiz application written in Python with SQLite for persistent storage. Users can register, login, take category- and difficulty-based quizzes, view a leaderboard, and import questions from a CSV file.

## 📦 Features

- 📝 User Registration & Login
- 📚 Question Bank with Category and Difficulty Levels
- ⏱️ 15-Second Timer Per Question
- 📊 Score Tracking and Leaderboard
- 📂 Import Questions from CSV
- 🧠 Quiz Customization by Category & Difficulty

## 🛠️ Tech Stack

- Python 3
- SQLite (via `sqlite3`)
- CSV File Parsing
- CLI-based Interaction

## 📂 File Structure

```plaintext
├── main.py                # Main application logic
├── quiz_app.db            # SQLite database (auto-created)
├── questions_imported.flag # Flag file to avoid re-importing CSV questions
└── quiz_csv.csv           # [You should provide this] CSV file with quiz questions
```

## 🧪 How to Run

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/quiz-app-python.git
cd quiz-app-python
```

2. **Place your CSV file**

Update the `CSV_FILE_PATH` in `main.py` to point to your quiz CSV file path:

```python
CSV_FILE_PATH = "C:\path\to\your\quiz_csv.csv"
```

3. **Run the application**

```bash
python main.py
```

4. **Navigate the Menu**

- `1` - Register
- `2` - Login & Take Quiz
- `3` - View Leaderboard
- `4` - Exit

## 📄 CSV Format

Your CSV should contain the following headers:

```csv
question,option_a,option_b,option_c,option_d,correct_option,category,difficulty
```

Example:

```csv
What is the capital of France?,Paris,Lyon,Marseille,Nice,A,Geography,Easy
```

## 🛡️ Security Note

- Passwords are stored in **plain text** for demonstration purposes. Please hash them using libraries like `bcrypt` or `hashlib` for production use.

## 🚀 Future Improvements

- Add password hashing & encryption
- Implement user sessions
- Add export-to-CSV feature for scores
- Web-based UI using Flask/Django

## 🧑‍💻 Author

**Animesh Kumar Singh**  
[GitHub](https://github.com/animesh713331) | aks.gecv27@gmail.com | +91 9508179290

---

🧠 Keep learning. Keep quizzing!
