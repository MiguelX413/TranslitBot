#!/usr/bin/env python3
import logging
import os
from typing import TextIO, Callable
import scriptcon
import re

try:
    import ujson

    json = ujson
except ModuleNotFoundError:
    try:
        import json
    except ModuleNotFoundError:
        print("json module not found, can't read dict")


from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.ext import (
    Updater,
    InlineQueryHandler,
    CommandHandler,
    CallbackContext,
)

url_regex = re.compile(
    r"\s?(((about|ftp(s)?|filesystem|git|ssh|http(s)?):(\/\/)?)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)\s?)"
)

if __name__ == "__main__":
    import argparse

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Runs TG bot")
    parser.add_argument(
        "token",
        action="store",
        # default=os.environ["TG_TOKEN"] if "TG_TOKEN" in os.environ else None,
        type=str,
        help="Telegram Token for the bot",
    )
    parser.add_argument(
        "dict",
        action="store",
        type=argparse.FileType("r"),
        help="Dictionary with which to transliterate",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enabled Debugging mode",
    )
    parser.add_argument(
        "--no-rich",
        action="store_false",
        dest="rich",
        help="Disables rich output",
    )
    parser.add_argument(
        "--log-file",
        action="store_true",
        dest="logfile",
        help="Output to log file",
    )
    parser_args = parser.parse_args()

    do_rich = True
    if parser_args.rich:
        try:
            import rich
            from rich.progress import track, Progress
            from rich.logging import RichHandler
        except ModuleNotFoundError:
            do_rich = False
    else:
        do_rich = False

    if do_rich:
        logging_handlers = [RichHandler(rich_tracebacks=True)]
    else:
        logging_handlers = [logging.StreamHandler()]

    if parser_args.logfile:
        logging_handlers.append(logging.FileHandler("TranslitBot.log"))

    logging.basicConfig(
        level=logging.DEBUG if parser_args.debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=logging_handlers,
    )

    logging.info(str(parser_args))
    logging.info("do_rich: " + str(do_rich))

    dictsfile: TextIO = parser_args.dict
    dictsdata = json.loads(dictsfile.read())
    dictsfile.close()
    logging.info(dictsfile.name)



def utf16len(string: str) -> int:
    return len(string.encode("UTF-16-le")) // 2


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Ка̄ла!\nカーラ゚！\nᨀᨕᨒ!")


def convert(text, dictionary) -> str:
    result = ""
    for x in url_separate(text):
        if url_regex.match(x) is None:
            result += scriptcon.convert(
                scriptcon.convert(x, dictsdata["Latin"]),
                dictionary,
            )
        else:
            result += x
    return result


def genfunc(dictionary) -> Callable[[Update, CallbackContext], None]:
    def function(update: Update, _: CallbackContext) -> None:
        if update.message.reply_to_message is not None:
            if update.message.reply_to_message.text is not None:
                text = update.message.reply_to_message.text
            elif update.message.reply_to_message.caption is not None:
                text = update.message.reply_to_message.caption
            else:
                text = ""
            update.message.reply_text(scriptcon.convert(text, dictionary))

    return function


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    cyrillicResult = ""
    katakanaResult = ""
    lontaraResult = ""
    latinResult = ""
    for x in [query]:
        if url_regex.match(x) is None:
            latinConversion = scriptcon.convert(x, dictsdata["Latin"])
            latinResult += latinConversion
            cyrillicResult += scriptcon.convert(latinConversion, dictsdata["Cyrillic"])
            katakanaResult += scriptcon.convert(latinConversion, dictsdata["Katakana"])
            lontaraResult += scriptcon.convert(latinConversion, dictsdata["Lontara"])
        else:
            latinResult += x
            cyrillicResult += x
            katakanaResult += x
            lontaraResult += x
    results = [
        InlineQueryResultArticle(
            id=1,
            title="Cyrillic",
            description=cyrillicResult,
            input_message_content=InputTextMessageContent(cyrillicResult),
        ),
        InlineQueryResultArticle(
            id=2,
            title="Katakana",
            description=katakanaResult,
            input_message_content=InputTextMessageContent(katakanaResult),
        ),
        InlineQueryResultArticle(
            id=3,
            title="Lontara",
            description=lontaraResult,
            input_message_content=InputTextMessageContent(lontaraResult),
        ),
        InlineQueryResultArticle(
            id=4,
            title="Latin",
            description=latinResult,
            input_message_content=InputTextMessageContent(latinResult),
        ),
    ]

    update.inline_query.answer(results, cache_time=30)


def main(token: str) -> None:
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("cyrillic", genfunc(dictsdata["Cyrillic"])))
    dispatcher.add_handler(CommandHandler("katakana", genfunc(dictsdata["Katakana"])))
    dispatcher.add_handler(CommandHandler("lontara", genfunc(dictsdata["Lontara"])))

    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main(parser_args.token)
