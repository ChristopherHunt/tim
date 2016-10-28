#!/usr/bin/python3

class Pack:
    'Represents a booster pack of cards in Magic the Gathering draft.'

    ## Represents a booster pack of Magic the Gathering cards.
    ## Cards is a list of cards
    def __init__(self, cards):
        self.cards = list(cards)  ## Copy by value

    def __str__(self):
        toString = ""
        for card in self.cards:
            toString += str(card) + '\n'
        return toString            

    ## Adds a card to the pack
    def add(self, card):
        self.cards.append(card)

    ## Returns the number of cards within the pack.
    def count(self):
        return len(self.cards)

    ## Removes the specified card from the pack.
    ##   card = the name of the card to be removed
    ## Returns true if the card was removed.
    def pick(self, card):
        if card in self.cards:
            self.cards.remove(card) 
            return True
        return False
