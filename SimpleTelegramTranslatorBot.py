# encoding: utf-8

import logging
import telegram
import urllib
import time
from urllib.error import URLError
from yandex_translate import YandexTranslate


translator = YandexTranslate('yandex-token')
def processIncomeMessages(bot, lastUpdateId):
    for update in bot.getUpdates(offset=lastUpdateId, timeout=10):
        chat_id = update.message.chat_id
        lastUpdateId = update.update_id + 1
        message = update.message.text

        response = ""
        sourceLang = translator.detect(message)
        if sourceLang == "en":
            response = "Your message is already in english!"
        else:
            doc = translator.translate(message, "en")
            if not "text" in doc:
                response = "I couldn't translate your message :("
            else:
                response = " ".join(doc["text"])
        if message:
            # Reply to the message
            bot.sendMessage(chat_id=chat_id,
                            text=response)
    return lastUpdateId


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    bot = telegram.Bot('telegram-token')  # Telegram Bot Authorization Token

    try:
        lastUpdateId = bot.getUpdates()[-1].update_id  # Get lastest update
    except IndexError:
        lastUpdateId = None

    while True:
        try:
            lastUpdateId = processIncomeMessages(bot, lastUpdateId)
        except telegram.TelegramError as e:
            # These are network problems with Telegram.
            if e.message in ("Bad Gateway", "Timed out"):
                time.sleep(1)
            elif e.message == "Unauthorized":
                # The user has removed or blocked the bot.
                lastUpdateId += 1
            else:
                raise e
        except URLError as e:
            # These are network problems on our end.
            time.sleep(1)


if __name__ == '__main__':
    main()
