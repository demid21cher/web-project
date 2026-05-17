from bs4 import BeautifulSoup
import requests
import time

from sqlite3 import IntegrityError, DatabaseError
from db import init_db, get_db_connection


def save_to_db(title, href, price):

    conn = get_db_connection()

    try:
        conn.execute(
            "INSERT INTO apple (title, href, price) VALUES (?, ?, ?)",
            (title, href, price),
        )

        conn.commit()

    except IntegrityError:
        print("Entry already exists")

    except DatabaseError as e:
        print(f"Database error: {e}")

    finally:
        conn.close()


if __name__ == "__main__":

    init_db()

    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, 6):

        print(f"Парсимо сторінку {page}")

        url = f"https://www.olx.ua/uk/list/q-Iphone/?page={page}"

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.find_all("div", class_="css-u2ayx9")

        for card in cards:

            title = card.find("h4", class_="css-wlcw7o")

            link = card.find("a", class_="css-1tqlkj0")

            price = card.find("p", class_="css-61fb99")

            if title and link and price:

                href = f"https://www.olx.ua{link["href"]}"

                save_to_db(
                    title.text.strip(),
                    href,
                    price.text.strip(),
                )

        time.sleep(5)

print("Парсинг завершено")
