#!/usr/bin/python3

import copy
import os
import sys
from collections import Counter

## Import path hacking to make this run referencing the modules it needs.
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                             os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.deck import Deck
from lib.pack_generator import PackGenerator

class AIValidator(object):
    'Class to run a set of specified comparisons between a datum deck and a\
    testing deck.'

    ## Takes in a pack_generator so it knows the context of all cards being
    ## passed in for future runs.
    def __init__(self, pack_gen):
      self._pack_gen = pack_gen

    def generate_deck_from_decklist(self, decklist):
      deck = Deck()
      for card_name in decklist:
        deck.add_card(self._pack_gen.get_card_from_name(card_name))
      return copy.deepcopy(deck)

    def get_percent_matching_cards(self, datum_decklist, test_decklist):
      ## Make a dictionary of card --> count for each deck 
      datum_decklist_counts = Counter(datum_decklist)
      test_decklist_counts = Counter(test_decklist)

      card_similarity_count = 0
      ## Count how many cards are the same in the two decks
      for name, datum_card_count in datum_decklist_counts.items():
        if name in test_decklist_counts.keys():
          test_card_count = test_decklist_counts[name]
          card_similarity_count += datum_card_count -\
                                   (datum_card_count - test_card_count)

      ## Return the ratio of card similarity
      return card_similarity_count / len(datum_decklist)

    def get_percent_color_matching(self, datum_decklist, test_decklist):
      ## Generate decks from the decklists
      datum_deck = self.generate_deck_from_decklist(datum_decklist)
      test_deck = self.generate_deck_from_decklist(test_decklist)

      ## Get the color distribution of each deck
      datum_deck_color_distribution = datum_deck.get_color_distribution_of_playables(150)
      test_deck_color_distribution = test_deck.get_color_distribution_of_playables(150)

      ## Take the difference between each of the deck's color distributions
      result = sum(x for x in [abs(x - y) for x, y in
                                    zip(datum_deck_color_distribution.values(),
                                        test_deck_color_distribution.values())])

      ## Return the sum of the differences of color distributions of the two
      ## decks.
      return 1 - result

    ## Runs comparisons between the datum and test decks and returns a
    ## dictionary of results to the caller.
    def run(self, datum_decklist, test_decklist):
      results = {}
      results['card_similarity'] =\
        self.get_percent_matching_cards(datum_decklist, test_decklist)
      results['color_similarity'] =\
        self.get_percent_color_matching(datum_decklist, test_decklist)
      return copy.deepcopy(results)
