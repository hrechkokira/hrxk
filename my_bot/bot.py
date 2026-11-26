
import telebot
import os
import random
from dotenv import load_dotenv
from telebot import types

# Завантажуємо змінні з файлу .env
load_dotenv()

# Отримуємо токен бота
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен BOT_TOKEN не знайдено!")

# Створюємо бота
bot = telebot.TeleBot(TOKEN)

# База даних загадок про тварин
animals = [
    {
        "question": "Яка тварина має найдовшу шию?",
        "answer": "жирафа",
        "hint": "Вона живе в Африці та харчується листям дерев.",
        "fact": "Язик жирафи може досягати приблизно 45 см."
    },
    {
        "question": "Яка тварина змінює колір шкіри?",
        "answer": "хамелеон",
        "hint": "Ця тварина має довгий липкий язик.",
        "fact": "Хамелеони можуть рухати очима незалежно одне від одного."
    },
    {
        "question": "Який птах не вміє літати, але чудово плаває?",
        "answer": "пінгвін",
        "hint": "Він живе переважно в Південній півкулі.",
        "fact": "Пінгвіни використовують крила як ласти під водою."
    },
    {
        "question": "Яка тварина має вісім щупалець?",
        "answer": "восьминіг",
        "hint": "Вона мешкає в морях та океанах.",
        "fact": "У восьминога три серця."
    },
    {
        "question": "Яка тварина спить догори ногами?",
        "answer": "кажан",
        "hint": "Це єдиний ссавець, здатний до активного польоту.",
        "fact": "Кажани орієнтуються в просторі за допомогою ехолокації."
    }
]

# Цікаві факти про тварин
facts = [
    "🐘 Слони можуть спілкуватися за допомогою низькочастотних звуків.",
    "🐬 Дельфіни мають власні характерні свисти.",
    "🦉 Сови можуть повертати голову приблизно на 270 градусів.",
    "🐙 У восьминога три серця.",
    "🦒 Жирафи мають унікальний візерунок плям.",
    "🐝 Бджоли передають інформацію про їжу за допомогою танцю."
]

# Головне меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.add(
        types.KeyboardButton("🔎 Відгадати тварину"),
        types.KeyboardButton("🧠 Цікавий факт")
    )

    markup.add(
        types.KeyboardButton("❓ Допомога")
    )

    return markup


# Команда старт
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🕵️ Вітаю у світі детективів тварин!\n\n"
        "Тут ти зможеш розгадувати загадки, "
        "дізнаватися цікаві факти та перевіряти свої знання.\n\n"
        "Обирай дію в меню!",
        reply_markup=main_menu()
    )


# Гра «Відгадай тварину»
@bot.message_handler(commands=["quiz"])
@bot.message_handler(func=lambda message: message.text == "🔎 Відгадати тварину")
def quiz(message):
    animal = random.choice(animals)

    # Зберігаємо загадку для конкретного користувача
    user_id = message.from_user.id
    user_questions[user_id] = animal

    markup = types.InlineKeyboardMarkup()

    hint_button = types.InlineKeyboardButton(
        "💡 Підказка",
        callback_data="hint"
    )

    markup.add(hint_button)

    bot.send_message(
        message.chat.id,
        "🕵️ ДЕТЕКТИВНЕ ЗАВДАННЯ\n\n"
        + animal["question"]
        + "\n\nНапиши свою відповідь!",
        reply_markup=markup
    )


# Зберігаємо активні загадки
user_questions = {}


# Обробка підказки
@bot.callback_query_handler(func=lambda call: call.data == "hint")
def hint(call):
    animal = user_questions.get(call.from_user.id)

    if animal:
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "💡 Підказка: " + animal["hint"]
        )
    else:
        bot.answer_callback_query(
            call.id,
            "Спочатку розпочни нову гру!"
        )


# Перевірка відповіді
@bot.message_handler(func=lambda message: message.from_user.id in user_questions)
def check_answer(message):
    animal = user_questions[message.from_user.id]

    if message.text.lower().strip() == animal["answer"]:
        bot.send_message(
            message.chat.id,
            "🎉 Правильно! Ти справжній детектив!\n\n"
            "🐾 Цікавий факт: " + animal["fact"]
        )

        del user_questions[message.from_user.id]

    else:
        bot.send_message(
            message.chat.id,
            "❌ Не зовсім правильно!\n"
            "Спробуй ще раз або скористайся підказкою 💡"
        )


# Випадковий цікавий факт
@bot.message_handler(commands=["fact"])
@bot.message_handler(func=lambda message: message.text == "🧠 Цікавий факт")
def animal_fact(message):
    fact = random.choice(facts)

    bot.send_message(
        message.chat.id,
        "🧠 Цікавий факт:\n\n" + fact
    )


# Допомога
@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == "❓ Допомога")
def help_command(message):
    bot.send_message(
        message.chat.id,
        "📚 Команди бота:\n\n"
        "/start — головне меню\n"
        "/quiz — розгадати загадку\n"
        "/fact — цікавий факт\n"
        "/help — допомога\n\n"
        "Успіхів у розслідуваннях! 🐾"
    )


# Обробка інших повідомлень
@bot.message_handler(content_types=["text"])
def unknown_message(message):
    bot.send_message(
        message.chat.id,
        "🤔 Я не зрозумів повідомлення.\n"
        "Скористайся меню або командою /help."
    )


# Запуск бота
if __name__ == "__main__":
    print("🕵️ Детективний світ тварин запущено!")

    bot.infinity_polling()
