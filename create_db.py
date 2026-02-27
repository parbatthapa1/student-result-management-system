import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "rms.db")

def create_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # ───────────────────────────────────────────────
    #  Core tables
    # ───────────────────────────────────────────────

    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            duration TEXT,
            charges TEXT,
            description TEXT
        )
    """)
    con.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            admission TEXT,
            course TEXT,          -- legacy column (being phased out)
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT
        )
    """)
    con.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            course TEXT,
            subject TEXT,
            marks_ob INTEGER,
            full_marks INTEGER,
            per REAL
        )
    """)
    con.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS enrollment(
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            roll INTEGER,
            cid INTEGER,
            UNIQUE(roll, cid)
        )
    """)
    con.commit()

    # ───────────────────────────────────────────────
    #  Authentication table (NEW - for login/register)
    # ───────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            uid     INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,           -- plain text (for learning project only)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    """)
    con.commit()

    # Optional: create a default admin user if table is empty
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, ("admin", "admin123"))   # ← Change this password in production!
        con.commit()
        print("Default admin user created: username = admin / password = admin123")

    # ───────────────────────────────────────────────
    #  Legacy migration (your existing code - kept as-is)
    # ───────────────────────────────────────────────
    try:
        cur.execute("PRAGMA table_info(student)")
        cols = [r[1] for r in cur.fetchall()]
        if "course" in cols:
            cur.execute("SELECT roll, course FROM student WHERE course IS NOT NULL AND TRIM(course) <> ''")
            rows = cur.fetchall()
            for roll, course_name in rows:
                cur.execute("SELECT cid FROM course WHERE name=?", (course_name,))
                res = cur.fetchone()
                if res:
                    cid = res[0]
                else:
                    cur.execute("INSERT OR IGNORE INTO course (name, duration, charges, description) VALUES (?, '', '', '')", (course_name,))
                    con.commit()
                    cur.execute("SELECT cid FROM course WHERE name=?", (course_name,))
                    cid = cur.fetchone()[0]
                cur.execute("INSERT OR IGNORE INTO enrollment (roll, cid) VALUES (?, ?)", (roll, cid))
                con.commit()
    except Exception as e:
        print("Migration warning:", str(e))

    con.close()

if __name__ == "__main__":
    create_db()
    print("Database created/updated at:", DB_PATH)