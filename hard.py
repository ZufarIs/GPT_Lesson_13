from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from dotenv import load_dotenv
import os
import uuid

# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')

lang = 'rus'


# INLINE
# форма inline клавиатуры
inline_frame = [[InlineKeyboardButton("English", callback_data="eng")],
                [InlineKeyboardButton("Русский", callback_data="rus")]]
# создаем inline клавиатуру
inline_keyboard = InlineKeyboardMarkup(inline_frame)

# функция-обработчик команды /start
async def start(update: Update, _):

    # прикрепляем inline клавиатуру к сообщению
    await update.message.reply_text('Select your language:', reply_markup=inline_keyboard)


# функция-обработчик команды /help
async def help(update, context):
    if lang == 'rus':
        reply = "Это бот говорит по-русски!"
    else:
        reply = "This bot speak english!"
    await update.message.reply_text(f"{reply} \U0001F539")


# функция-обработчик текстовых сообщений
async def text(update, context):
    if lang == 'rus':
        reply = "Мы получили от тебя текстовое соообщение!"
    else:
        reply = "We've received a text message from you!"
    await update.message.reply_text(reply)


# функция-обработчик сообщений с изображениями
async def image(update, context):
    if lang == 'rus':
        reply = "Фотография сохранена!"
    else:
        reply = "Photo saved!"
    await update.message.reply_text(reply)
    file = await update.message.photo[-1].get_file()
    
    # сохраняем изображение на диск
    os.makedirs("photos", exist_ok=True)
    await file.download_to_drive("photos/photo_" + str(uuid.uuid4()) + ".jpg")


# функция-обработчик голосовых сообщений
async def voice(update, context):
    if lang == 'rus':
        reply = "Мы получили от тебя голосовое соообщение!"
    else:
        reply = "We’ve received a voice message from you!"
    await update.message.reply_text(reply)

# функция-обработчик нажатий на кнопки
async def button(update: Update, _):

    # получаем callback query из update
    query = update.callback_query
    global lang
    lang = query.data
    
    # редактируем сообщение после нажатия
    if lang == 'rus':
        reply = "Вы выбрали русский язык!"
    else:
        reply = "You've selected english!"
    await query.edit_message_text(text=reply)


def main():

    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик команды /help
    application.add_handler(CommandHandler("help", help))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик сообщений с фотографиями
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # добавляем CallbackQueryHandler (только для inline кнопок)
    application.add_handler(CallbackQueryHandler(button))

    # запускаем бота (нажать Ctrl-C для остановки бота)
    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()