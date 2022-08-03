from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes
from qas import load_bert, single_question_bot


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'{single_question_bot(update.message.text.lower())}')


if __name__ == '__main__':
    load_bert()
    app = ApplicationBuilder().token("5400690236:AAGMSHTY-BCt5Z1nCVgxeZ0bhlSWRnmLLpE").build()
    app.add_handler(MessageHandler(None, ask))
    app.run_polling()
