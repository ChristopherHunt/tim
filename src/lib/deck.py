#!/usr/bin/python3

import copy
import sys

from lib.card import Card

class Deck:
    'Represents a deck of Magic the Gathering cards.'

    def __init__(self):
        self.cards = []

    def __str__(self):
        to_string = ''
        for card in self.cards:
            to_string += '1 ' + str(card.name) + '\n'
        return to_string

    ## Adds the specified card to the deck.
    def add_card(self, card):
        self.cards.append(copy.copy(card))

    ## Returns a dictionary representing the color distribution of the cards in
    ## the deck. This distribution is represented as a mapping of card color to
    ## the decimal version of that color's percentage in the deck.
    ## Aka:
    ##          'White' : 0.6
    ## would mean that 60% of the cards in the deck are white.
    def get_color_distribution(self):
      return self.get_color_distribution_of_playables(100000)

    ## Returns a dictionary representing the color distribution of the cards in
    ## the deck. This distribution is represented as a mapping of card color to
    ## the decimal version of that color's percentage in the deck.
    ## Aka:
    ##          'White' : 0.6
    ## would mean that 60% of the cards in the deck are white. Note that this
    ## ranking only takes into account cards that are less than or equal to the
    ## specified rank in order to try and only rank by playables.
    def get_color_distribution_of_playables(self, rank):
      colors = {'White' : 0.0,
                'Blue'  : 0.0,
                'Black' : 0.0,
                'Red'   : 0.0,
                'Green' : 0.0,
                'Colorless': 0.0}

      playables_count = 0

      ## Only run these computations if there are cards in the deck.
      if self.cards:
        ## Tally all the color counts.
        for card in self.cards:
          if card.rank <= rank:
            playables_count += 1
            for color in card.colors:
              if card.colors[color] == True:
                colors[color] += 1

        if playables_count:
          for color in colors:
            colors[color] /= playables_count

      return copy.deepcopy(colors)
