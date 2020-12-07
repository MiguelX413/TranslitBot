import logging
from uuid import uuid4
import scriptcon
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

def start(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /start is issued."""
	update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /help is issued."""
	update.message.reply_text('Help!')


def inlinequery(update: Update, context: CallbackContext) -> None:
	"""Handle the inline query."""
	query = update.inline_query.query
	cyrillicResult = scriptcon.toCyrillic(query)
	katakanaResult = scriptcon.toKatakana(query)
	lontaraResult = scriptcon.toLontara(query)
	results = [
		InlineQueryResultArticle(
			id=uuid4(), title="Cyrillic", description=cyrillicResult, input_message_content=InputTextMessageContent(cyrillicResult)
		),
		InlineQueryResultArticle(
			id=uuid4(), title="Katakana", description=katakanaResult, input_message_content=InputTextMessageContent(katakanaResult)
		),
		InlineQueryResultArticle(
			id=uuid4(), title="Lontara", description=lontaraResult, input_message_content=InputTextMessageContent(lontaraResult)
		)
	]

	update.inline_query.answer(results,cache_time=30)

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(InlineQueryHandler(inlinequery))
updater.start_polling()
updater.idle()
