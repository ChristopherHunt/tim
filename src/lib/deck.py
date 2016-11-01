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
            to_string += str(card) + '\n'
        return to_string

    ## Adds the specified card to the deck.
    def add_card(self, card):
        self.cards.append(copy.copy(card))
