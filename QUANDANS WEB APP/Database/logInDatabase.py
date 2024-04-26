import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT,
                password TEXT
            )
        """)
        self.conn.commit()

    def insert_user(self, username, email, password):
        try:
            self.cursor.execute("""
               INSERT INTO users (username, email, password) 
               VALUES (?, ?, ?)
            """, (username, email, password))
            print("User added")
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("A backend error when adding a new user occurred because the user already exists")

    def showall(self):
        STATE = True
        if STATE:
            ev = self.cursor.execute("""
                    SELECT * FROM users 
                """)
            return ev.fetchall()
        else:
            print("Function usage permission denied")

    def check_user(self, username, email, password):
        self.cursor.execute("""
            SELECT * FROM users WHERE username = ? AND email = ? AND password = ? 
        """, (username, email, password))
        user = self.cursor.fetchone()
        print(user)
        return user is not None

    def close(self):
        self.conn.close()

