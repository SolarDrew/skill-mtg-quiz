import random
import logging

from opsdroid.matchers import match_regex, match_cron
from mtgsdk import Card

def setup(opsdroid):
    logging.info("Loaded MtG Bot")


@match_cron('* * * * *')
@match_regex('give me a card', case_sensitive=False)
async def select_card(opsdroid, config, message):
    current_set = config['current_set']
    allcards = Card.where(set=current_set).all()

    message.respond(f'{random.choice(allcards).name}')
