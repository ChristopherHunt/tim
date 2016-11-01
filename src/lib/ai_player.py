#!/usr/bin/python3

from lib.player import Player

class AIPlayer(Player):
    'Class to define an AI player for a Magic the Gathering draft.'

    def __init__(self, player_name, ai_core):
        Player.__init__(self, player_name)
        self.ai_core = ai_core

    ## Chooses a card from the pack as specified by the bot's ai_core.
    def pick_card_from_pack(self, pack):
        self.deck.add_card(self.ai_core.pick_card_from_pack(pack))
