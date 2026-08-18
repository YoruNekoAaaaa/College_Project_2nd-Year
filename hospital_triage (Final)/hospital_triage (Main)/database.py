import sqlite3
import hashlib

DB_NAME = "hospital_users.db"


# =========================================================
# CONNECT DATABASE
# =========================================================
def connect():

    conn = sqlite3.connect(DB_NAME)

    return conn


# =========================================================
# HASH PASSWORD
# =========================================================
def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# CREATE USERS TABLE
# =========================================================
def create_users_table():

    with connect() as conn:

        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS users (

            username TEXT PRIMARY KEY,

            password TEXT NOT NULL
        )
        """)

        conn.commit()


# =========================================================
# CREATE PATIENT TABLE
# =========================================================
def create_patients_table():

    with connect() as conn:

        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS patients (

            id TEXT PRIMARY KEY,

            username TEXT,

            name TEXT,

            age INTEGER,

            symptoms TEXT,

            pain_level INTEGER,

            priority INTEGER,

            status TEXT DEFAULT 'waiting'
        )
        """)

        conn.commit()


# =========================================================
# REGISTER USER
# =========================================================
def register_user(username, password):

    username = username.strip()

    if not username or not password:
        return False

    try:

        with connect() as conn:

            c = conn.cursor()

            # CHECK IF USER EXISTS
            c.execute(
                "SELECT username FROM users WHERE username=?",
                (username,)
            )

            existing = c.fetchone()

            if existing:
                print("Username already exists")
                return False

            # INSERT USER
            c.execute(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?)
                """,
                (
                    username,
                    hash_password(password)
                )
            )

            conn.commit()

            print("Account created successfully")

            return True

    except Exception as e:

        print("REGISTER ERROR:", e)

        return False


# =========================================================
# LOGIN USER
# =========================================================
def login_user(username, password):

    try:

        with connect() as conn:

            c = conn.cursor()

            c.execute(
                "SELECT password FROM users WHERE username=?",
                (username,)
            )

            row = c.fetchone()

            if row:

                stored_password = row[0]

                if stored_password == hash_password(password):

                    return True

            return False

    except Exception as e:

        print("LOGIN ERROR:", e)

        return False


# =========================================================
# CHANGE PASSWORD
# =========================================================
def change_password(username, new_password):

    try:

        with connect() as conn:

            c = conn.cursor()

            c.execute(
                """
                UPDATE users
                SET password=?
                WHERE username=?
                """,
                (
                    hash_password(new_password),
                    username
                )
            )

            conn.commit()

    except Exception as e:

        print("CHANGE PASSWORD ERROR:", e)


# =========================================================
# DELETE ACCOUNT
# =========================================================
def delete_account(username):

    try:

        with connect() as conn:

            c = conn.cursor()

            c.execute(
                "DELETE FROM users WHERE username=?",
                (username,)
            )

            conn.commit()

    except Exception as e:

        print("DELETE ERROR:", e)


# =========================================================
# SAVE PATIENT
# =========================================================
def save_patient(username, p):

    try:

        with connect() as conn:

            c = conn.cursor()

            c.execute("""
            INSERT INTO patients
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (

                p.id,
                username,
                p.name,
                p.age,
                p.symptoms,
                p.pain_level,
                p.priority,
                "waiting"
            ))

            conn.commit()

            return True

    except Exception as e:

        print("SAVE PATIENT ERROR:", e)

        return False


# =========================================================
# GET PATIENTS
# =========================================================
def get_patients(username):
    try:
        with connect() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM patients")
            return c.fetchall()
    except Exception as e:
        print("GET PATIENT ERROR:", e)
        return []


# =========================================================
# MARK PATIENT TREATED
# =========================================================
def mark_patient_treated(patient_id):

    try:

        with connect() as conn:

            c = conn.cursor()

            c.execute(
                """
                UPDATE patients
                SET status='treated'
                WHERE id=?
                """,
                (patient_id,)
            )

            conn.commit()

    except Exception as e:

        print("TREAT ERROR:", e)
# =========================================================
# CLEAR WAITING PATIENTS
# =========================================================
def clear_waiting_patients(username):

    try:

        with connect() as conn:

            c = conn.cursor()

            c.execute(
                """
                DELETE FROM patients
                WHERE status='waiting'
                """,
                (username,)
            )

            conn.commit()

            print("Waiting patients cleared")

    except Exception as e:

        print(
            "CLEAR WAITING ERROR:",
            e
        )