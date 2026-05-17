from models import User, Information
from db import init_db


def main():
    permission = False
    user_session = None

    while True:
        print("=" * 50)
        input_task = (
            input(
                "Enter '1' to create a new account\n"
                "Enter '2' to access an existing account\n"
                "Enter '3' registration no web-site\n"
                "Enter '4' to access to web-site\n"
                "Enter '5' to exit\n"
            )
            .strip()
            .lower()
        )

        if input_task == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            user = User(username, password, email)
            message = user.register()
            print(message)

        elif input_task == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = User(username, password, "")
            success, message = user.login(username, password)
            print(message)
            if success:
                permission = True
                user_session = user.get_id()

        elif input_task == "3":
            if not permission:
                print("Please log in first.")
                continue
            title_site = input("Enter the title of the site: ")
            login = input("Enter the login for the site: ")
            password_site = input("Enter the password for the site: ")
            input_type = input("Enter the type of input (email, FaceBook, Apple): ")
            info = Information(
                title_site, login, password_site, input_type, user_session
            )
            print(info.create_information())

        elif input_task == "4":
            if not permission:
                print("Please log in first.")
                continue
            user.print_user_info()

        elif input_task == "5":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    init_db()
    main()
