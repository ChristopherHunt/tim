#!/usr/bin/python3

import copy
import os
import sys

## Import path hacking to make this run referencing the modules it needs.
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                             os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.ai_core import AICore
from lib.ai_player import AIPlayer
from lib.pack_generator import PackGenerator

class AITester(object):
    'Class to run a set of specified packs through an AI and record what picks it makes.'

    ## Takes in a pack_generator so it knows the context of all cards being
    ## passed in for future runs.
    def __init__(self, pack_gen):
      self._pack_gen = pack_gen

    ## Creates an AIPlayer which picks cards based on the logic inside the
    ## passed in ai_core, and then runs each of the serialized_draft picks
    ## through that AI's logic. Returns a tuple, with the first value being the
    ## deck that the AI ideally would have created (which was encoded in the
    ## serialized_draft file as the first value in each list), and the second
    ## value in the tuple is the actual deck of cards the bot picked.
    def run(self, ai_core, serialized_draft):
      ## Create an AIPlayer to wrap the passed in AICore
      ai_player = AIPlayer('', ai_core)

      ## List of datum picks
      datum_picks = []

      ## For each serialized_pack choice in the input
      for serialized_pack in serialized_draft:
        ## Split the serialized_pack up into a list of card_numbers
        serialized_pack.replace(' ', '')
        card_num_list = serialized_pack.split(',')

        ## Copy the first value and record that as the correct datum pick
        datum_card_num = int(card_num_list.pop(0))
        datum_card = self._pack_gen.get_card_from_number(datum_card_num)
        datum_picks.append(datum_card.name)

        ## Parse the serialized_pack into a Pack object
        pack = self._pack_gen.convert_card_nums_to_pack(card_num_list)

        ## Have the ai_player pick a card from the pack
        ai_player.pick_card_from_pack(pack)

        ## Parse out only the card names that the ai_player picked
        ai_picks = [card.name for card in ai_player.deck.cards]

      return copy.deepcopy(datum_picks), copy.deepcopy(ai_picks)
