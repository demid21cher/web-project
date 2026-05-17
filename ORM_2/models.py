from sqlite3 import IntegrityError, DatabaseError
from db import get_db_connection
import hashlib


class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.db = get_db_connection()

    def register(self):
        try:
            self.db.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (
                    self.username,
                    hashlib.sha256(self.password.encode()).hexdigest(),
                    self.email,
                ),
            )
            self.db.commit()
            return "Registration successful"
        except IntegrityError:
            return "Username or email already exists"
        except DatabaseError as e:
            return f"Database error: {str(e)}"

    def login(self, username, password):
        try:
            result = self.db.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, hashlib.sha256(password.encode()).hexdigest()),
            ).fetchone()
            if result:
                return True, "Login successful"
            else:
                return False, "Invalid username or password"
        except DatabaseError as e:
            return False, f"Database error: {str(e)}"

    def get_id(self):
        try:
            result = self.db.execute(
                "SELECT id FROM users WHERE username = ?", (self.username,)
            ).fetchone()
            return result["id"] if result else None
        except DatabaseError as e:
            print(f"Database error: {str(e)}")
            return None

    def print_user_info(self):
        result = self.db.execute(
            "SELECT title_site FROM information AS info JOIN users AS u ON info.user_id = u.id WHERE u.username = ?",
            (self.username,),
        ).fetchall()
        if result:
            print(f"User: {self.username}")
            for row in result:
                print(f"Title Site: {row['title_site']}")
        else:
            print("No information found for this user.")


class Information:
    def __init__(self, title_site, login, password, input_type, user_id):
        self.title_site = title_site
        self.login = login
        self.password = password
        self.input_type = input_type
        self.user_id = user_id
        self.db = get_db_connection()

    def create_information(self):
        try:
            self.db.execute(
                "INSERT INTO information (title_site, login, password, input_type, user_id) VALUES (?, ?, ?, ?, ?)",
                (
                    self.title_site,
                    self.login,
                    hashlib.sha256(self.password.encode()).hexdigest(),
                    self.input_type,
                    self.user_id,
                ),
            )
            self.db.commit()
            return "Information created successfully"
        except DatabaseError as e:
            return f"Database error: {str(e)}"
