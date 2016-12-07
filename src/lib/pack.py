#!/usr/bin/python3

import copy
import sys

from lib.card import Card

class Pack:
    'Represents a booster pack of cards in Magic the Gathering draft.'

    ## Represents a booster pack of Magic the Gathering cards.
    ## Cards is a list of cards
    def __init__(self, cards):
        self.cards = list(cards)  ## Copy by value
        self.highest_ranked_card = None
        self._find_highest_ranked_card_in_pack()

    def __str__(self):
        to_string = ''
        for card in self.cards:
            to_string += str(card) + '\n'
        return to_string            

    def card_names(self):
        card_names = []
        for card in self.cards:
            card_names.append(card.name)
        return copy.deepcopy(card_names)

    ## Finds the highest ranked card in the pack and updates the 
    ## self.highest_ranked_card reference to point to that card.
    def _find_highest_ranked_card_in_pack(self):
        self.highest_ranked_card = None
        if len(self.cards) > 0:
            ## Find the highest ranked card in the pack
            self.highest_ranked_card = self.cards[0]
            for card in self.cards[1:]:
                if card.rank < self.highest_ranked_card.rank:
                    self.highest_ranked_card = card

    ## Adds a card to the pack and update the highest_ranked_card if appropriate
    def add(self, card):
        self.cards.append(copy.deepcopy(card))  ## Copy by value

        ## Adjust highest card ranking in the pack if the new card is higher
        ## ranked than any other card in the pack.
        if not self.highest_ranked_card or \
          self.highest_ranked_card and card.rank < self.highest_ranked_card.rank:
            self.highest_ranked_card = self.cards[-1]  ## The new card

    ## Returns the number of cards within the pack.
    def count(self):
        return len(self.cards)
        
    def get_card_at_index(self, index):
        return copy.deepcopy(self.cards[index])

    ## Returns True if the specified Card is in the pack.
    def has_card(self, target_card):
      for card in self.cards:
        if card.number == target_card.number: 
          return True
      return False

    ## Removes the specified card from the pack.
    ##   card = a reference to a card to pick out of the pack
    ## Returns True if the card was removed from the pack.
    def pick_card(self, card):
        if card in self.cards:
            self.cards.remove(card) 
            if card.rank == self.highest_ranked_card.rank:
                self._find_highest_ranked_card_in_pack()
            return True
        return False

    ## Returns a string representing the serialized pack. This string has the
    ## following format:
    ##  highest_ranked_card_number, 1st_card_num, 2nd_card_num, ... nth_card_num
    ## where the highest_ranked_card_number is the number of the card in the
    ## pack with the highest ranking. Returns an empty string if the pack is
    ## empty.
    def serialize(self):
        serialized_pack = ''
        if len(self.cards) > 0:
            serialized_pack += str(self.highest_ranked_card.number)
            for card in self.cards:
                serialized_pack += ', ' + str(card.number)
        return serialized_pack
