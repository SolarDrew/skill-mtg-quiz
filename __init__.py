import random
import logging

from opsdroid.message import Message
from opsdroid.matchers import match_regex, match_crontab
from mtgsdk import Card


def card_from_booster(mtgset):
    r = random.randint(1, 14)
    if r < 11:
        rarity = 'common'
    elif r < 14:
        rarity = 'uncommon'
    else:
        if random.randint(1, 8) == 8:
            rarity = 'rare'
        else:
            rarity = 'mythic rare'

    cards = Card.where(set=mtgset).where(rarity=rarity)

    return random.choice(cards.all()).name


def setup(opsdroid):
    logging.info("Loaded MtG Bot")


@match_regex('give me a card', case_sensitive=False)
async def select_card(opsdroid, config, message):
    current_set = config['current_set']
    card = card_from_booster(current_set)

    await message.respond(f'{card}')


# @match_crontab('0 9,11,13,15,17,19 * * *', timezone='Europe/London')
@match_crontab('* * * * *', timezone='Europe/London')
async def auto_card(opsdroid, config, message):
    current_set = config['current_set']
    card = card_from_booster(current_set)

    # Get the default connector
    connector = opsdroid.default_connector

    # Get the default room for that connector
    room = connector.default_room

    # Create an empty message to respond to
    empty_message = Message("", None, room, connector)
    await empty_message.respond('This is a test, this should only get sent once') #f'{card}')


@match_regex('show me (?P<cardname>.*)', case_sensitive=False)
async def show_card(opsdroid, config, message):
    match = message.regex.group
    name = match('cardname')
    card = Card.where(set=config['current_set']).where(name=name).all()[0]

    await message.respond(card.image_url)
