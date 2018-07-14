import random
import logging

from opsdroid.matchers import match_regex, match_crontab
from mtgsdk import Card


def setup(opsdroid):
    logging.info("Loaded MtG Bot")


@match_regex('give me a card', case_sensitive=False)
@match_crontab('0 9,11,13,15,17,19 * * *', timezone='Europe/London')
async def select_card(opsdroid, config, message):
    current_set = config['current_set']
    allcards = Card.where(set=current_set).all()

    await message.respond(f'{random.choice(allcards).name}')
