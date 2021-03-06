#!/usr/bin/python3

from lib.ai_core import AICore

class DummyAI(AICore):
    'Test class to implement AI core.'

    def __init__(self):
        AICore.__init__(self, 'Dummy')

    ## Picks a card from the pack and returns it to the bot that called it.
    def pick_card_from_pack(self, deck, pack):
        ## Always try and pick the first card in the pack
        card = pack.get_card_at_index(0)

        ## Return the card to the calling AI bot
        if pack.pick_card(card):
            return card
        else:
            raise ValueError
