import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters


TOKEN = '7442357762:AAHENaDi-sx5Ta1gpLTRcQY4ihMM-dCxExs'

# Функція, яка викликається при старті бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привіт! Я генератор паролів. Використовуйте команду /generate, щоб отримати новий пароль.'
    )

# Функція для генерації пароля
def generate_password(length: int = 12, use_special: bool = True) -> str:
    characters = string.ascii_letters + string.digits
    if use_special:
        characters += string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Функція, яка викликається при команді /generate
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Введіть бажану довжину пароля:')

# Функція для обробки введеної довжини пароля
async def handle_length(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        length = int(update.message.text)
    except ValueError:
        await update.message.reply_text('Будь ласка, введіть правильне число для довжини пароля.')
        return

    if length < 6:
        await update.message.reply_text('Довжина пароля повинна бути не меншою за 6 символів.')
        return

    # Збереження довжини пароля у даних користувача
    context.user_data['length'] = length

    # Створення кнопок для вибору використання спеціальних символів
    keyboard = [
        [
            InlineKeyboardButton("Так", callback_data='yes'),
            InlineKeyboardButton("Ні", callback_data='no'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Чи хочете ви використовувати спеціальні символи в паролі?', reply_markup=reply_markup
    )

# Функція для обробки натискання кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    length = context.user_data.get('length', 12)
    use_special = query.data == 'yes'

    # Генерація пароля з урахуванням налаштувань
    password = generate_password(length, use_special)
    await query.edit_message_text(text=f'Ваш новий пароль: {password}')

# Основна функція для запуску бота
def main() -> None:
    # Створення додатку
    application = Application.builder().token(TOKEN).build()

    # Додавання обробників команд та повідомлень
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_length))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
