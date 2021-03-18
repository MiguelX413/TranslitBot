if __name__ == "__main__":
    import logging
    import os
    import scriptcon
    import re
    from telegram import (
        InlineQueryResultArticle,
        ParseMode,
        InputTextMessageContent,
        Update,
    )
    from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
    from telegram.utils.helpers import escape_markdown
    import json

    import argparse
    parser = argparse.ArgumentParser(description="Generate dictionary data")
    parser.add_argument("-r", "--rich", action=argparse.BooleanOptionalAction, default=True)
    do_rich = parser.parse_args().rich

    if do_rich:
        try:
            import rich
            from rich.progress import track, Progress
            from rich.logging import RichHandler
        except ModuleNotFoundError:
            do_rich = False

    url_regex = re.compile(
        r"\s?(((about|ftp(s)?|filesystem|git|ssh|http(s)?):(\/\/)?)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)\s?)"
    )

    def url_separate(text):
        working_text = text
        results = []
        if url_regex.search(text) is not None:
            while url_regex.search(working_text) is not None:
                partitions = working_text.partition(
                    url_regex.search(working_text).group(0)
                )
                results.append(partitions[0])
                results.append(partitions[1])
                working_text = partitions[2]
            else:
                results.append(working_text)
            return results
        else:
            return [text]

    token = os.environ["TG_TOKEN"]
    try:
        with open("dict.json", "r") as f:
            dictdata = json.loads(f.read())
    except FileNotFoundError:
        print("ERROR: No dict.json found, attempting to make one")
        try:
            import dictgen
        except ModuleNotFoundError:
            print("No dictgen.py found, unable to generate dict.json, exiting script")
            exit()
        with open("dict.json", "r") as f:
            dictdata = json.loads(f.read())

    def inlinequery(update: Update, context: CallbackContext) -> None:
        """Handle the inline query."""
        query = update.inline_query.query
        cyrillicResult = ""
        katakanaResult = ""
        lontaraResult = ""
        latinResult = ""
        for x in url_separate(query):
            if url_regex.match(x) is None:
                latinConversion = scriptcon.convert(x, dictdata["Latin"])
                latinResult += latinConversion
                cyrillicResult += scriptcon.convert(
                    latinConversion, dictdata["Cyrillic"]
                )
                katakanaResult += scriptcon.convert(
                    latinConversion, dictdata["Katakana"]
                )
                lontaraResult += scriptcon.convert(latinConversion, dictdata["Lontara"])
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

    logging_args = {
        "level": logging.DEBUG,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    }
    if do_rich:
        logging_args["handlers"]=[RichHandler(rich_tracebacks=True)]
    logging.basicConfig(**logging_args)

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()
