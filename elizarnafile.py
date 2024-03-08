pip install python-telegram-bot

BOT_TOKEN = '7026744232:AAEOHjflTJynz0ptzr5E-akkL4VceF0pkpE'

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

questions = ["My name ___ Vova", "I ___ a coder", "I live ___ Moscow", "I have ___ car"]
answers = ["is", "am", "in", "a"]

score = 0
points = 0
attempts = 3
points_max = len(questions) * 3

# States for conversation
START, NAME, QUIZ = range(3)

def start(update, context):
    update.message.reply_text(
        """Привет! Предлагаю проверить свои знания английского! Нажми /ready, чтобы начать!"""
    )
    return START

def ready(update, context):
    update.message.reply_text("Отлично! Напиши, как тебя зовут:")
    return NAME

def get_name(update, context):
    user_name = update.message.text
    context.user_data['name'] = user_name
    update.message.reply_text(f"Привет, {user_name}! Начинаем тренировку!")
    return QUIZ

def quiz(update, context):
    index = context.user_data.get('index', 0)
    correct_answer = answers[index]

    while attempts > 0:
        update.message.reply_text(questions[index])
        user_answer = update.message.text.lower()

        if user_answer == correct_answer:
            update.message.reply_text(f"Ответ верный! Вы получаете {attempts} баллов!")
            context.user_data['points'] = context.user_data.get('points', 0) + attempts
            context.user_data['score'] = context.user_data.get('score', 0) + 1
            break
        else:
            attempts -= 1
            if attempts > 0:
                update.message.reply_text(f"Неверно. Осталось попыток: {attempts}, попробуйте еще раз!")
            else:
                update.message.reply_text(f"Увы, но нет. Правильный ответ: {correct_answer}")
                break

    attempts = 3  # Reset attempts for the next question

    context.user_data['index'] = index + 1

    if index == len(questions) - 1:
        result_of_answers = round(context.user_data.get('points', 0) / points_max * 100, 2)
        update.message.reply_text(
            f"""Вот и всё, {context.user_data.get('name', '')}!
            Вы ответили на {context.user_data.get('score', 0)} вопросов из {len(questions)} верно.
            Вы заработали {context.user_data.get('points', 0)} баллов.
            Это {result_of_answers} процентов."""
        )
        context.user_data.clear()
        return START
    else:
        return QUIZ

def cancel(update, context):
    update.message.reply_text("Кажется, вы не хотите играть. Очень жаль.")
    context.user_data.clear()
    return START

def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [CommandHandler('ready', ready)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            QUIZ: [MessageHandler(Filters.text & ~Filters.command, quiz)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
