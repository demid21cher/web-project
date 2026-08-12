import telebot
from telebot import types
from config import TOKEN
from bank import Bank
from converter import Converter

bank = Bank()
converter = Converter()

bot = telebot.TeleBot(TOKEN)


# --- START ---
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Вітаю Я Бот Конвертер Валют:" "\n\n Виберіть валюту, яку хочете конвертувати",
        reply_markup=menu_currency(),
    )


# --- ВИБІР ВАЛЮТИ (ЗВІДКИ) ---
@bot.message_handler(func=lambda message: message.text in ["UAH", "USD", "EUR"])
def get_currency_from(message):
    currency_from = message.text

    remove_markup = types.ReplyKeyboardRemove()

    msg = bot.send_message(message.chat.id, "Введіть суму:", reply_markup=remove_markup)

    bot.register_next_step_handler(msg, get_balance, currency_from)


# --- ВВІД СУМИ ---
def get_balance(message, currency_from):
    try:
        balance_from = float(message.text)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Введіть число!")
        bot.register_next_step_handler(msg, get_balance, currency_from)
        return
    msg = bot.send_message(
        message.chat.id,
        "Виберіть валюту конвертації:",
        reply_markup=menu_currency(),
    )

    bot.register_next_step_handler(msg, get_currency_to, currency_from, balance_from)


# --- ВИБІР ВАЛЮТИ (КУДИ) ---
def get_currency_to(message, currency_from, balance_from):
    if message.text not in ["UAH", "USD", "EUR"]:
        msg = bot.send_message(message.chat.id, "Оберіть валюту з кнопок!")
        bot.register_next_step_handler(
            msg, get_currency_to, currency_from, balance_from
        )
        return

    currency_to = message.text

    try:
        balance_to = converter.convert(balance_from, currency_from, currency_to)
    except Exception:
        bot.send_message(message.chat.id, "Помилка конвертації")
        return

    data = {
        "currency_from": currency_from,
        "currency_to": currency_to,
        "balance_from": balance_from,
        "balance_to": balance_to,
    }

    bank.add_operation(data)

    bot.send_message(
        message.chat.id,
        f"{balance_from} {currency_from} => {round(balance_to, 2)} {currency_to}",
    )

    bot.send_message(
        message.chat.id,
        "Нова операція:",
        reply_markup=menu_currency(),
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    text = (
        "💱 *Бот конвертації валют*\n\n"
        "📌 *Як користуватись:*\n"
        "1. Обери валюту, з якої конвертувати\n"
        "2. Введи суму\n"
        "3. Обери валюту, в яку перевести\n\n"
        "🔄 *Приклад:*\n"
        "`100 UAH -> USD`\n\n"
        "📊 *Команди:*\n"
        "/start — запуск бота\n"
        "/help — ця довідка\n"
        "/list — останні 5 операцій\n\n"
        "🚀 Просто почни — і бот проведе тебе через процес"
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=menu_currency(),
    )


@bot.message_handler(commands=["list"])
def list(message):
    operations = bank.show_operations()

    text = "Останні 5 операцій:\n\n"

    for currency_from, balance_from, balance_to, currency_to in operations:
        text += (
            f"{balance_from} {currency_from} => {round(balance_to, 2)} {currency_to}\n"
        )

    bot.send_message(message.chat.id, text)


# --- МЕНЮ ---
def menu_currency():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("UAH")
    btn2 = types.KeyboardButton("USD")
    btn3 = types.KeyboardButton("EUR")

    markup.add(btn1, btn2, btn3)

    return markup


# --- ЗАПУСК ---
bot.infinity_polling()
