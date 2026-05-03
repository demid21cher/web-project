from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy as db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


engine = create_engine("sqlite:///example.db")
conn = engine.connect()

metadata = db.MetaData()

Users = db.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(255), unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("email", String(255), unique=True, nullable=False),
)

metadata.create_all(engine)


class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def register(self):
        try:
            query = db.insert(Users).values(
                username=self.username, password=self.password, email=self.email
            )
            conn.execute(query)
            conn.commit()
            return "Registration successful"
        except IntegrityError as e:
            conn.rollback()
            return "Error: User with this username or email already exists"
        except SQLAlchemyError as e:
            conn.rollback()
            return f"Database error: {str(e.__dict__.get('orig', e))}"

    def login(self, username, password):
        query = db.select(Users).where(
            (Users.c.username == username) & (Users.c.password == password)
        )
        result = conn.execute(query).fetchone()
        if result:
            return True, "Login successful"
        else:
            return False, "Invalid username or password"


def main():
    input_task = (
        input(
            "Enter '1' to create a new account\n Enter '2' to access an existing account\n Enter '3' to exit\n"
        )
        .strip()
        .lower()
    )
    if input_task == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter email: ")
        user = User(username, password, email)
        print(user.register())
    elif input_task == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = User(username, password, "")
        success, message = user.login(username, password)
        print(success, message)
    elif input_task == "3":
        print("Exiting...")
    else:
        print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
