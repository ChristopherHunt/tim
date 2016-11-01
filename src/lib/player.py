#!/usr/bin/python3

from lib.deck import Deck

class Player(object):
    'Interface which defines a player.'

    def __init__(self, player_name):
        self.player_name = player_name
        self.deck = Deck()

    def pick_card_from_pack(self, pack):
         raise NotImplementedError('pick_card_from_pack not implemented!')

    ## Prints the contents of the player's deck to the specified file.
    def print_deck_to_file(self, output_file):
        to_string = self.player_name + '\n'
        for x in range(0, len(self.player_name)):
            to_string += '-'
        to_string += '\n'
        to_string += str(self.deck)
        to_string += '\n\n'

        with open(output_file, 'a') as out_file:
            out_file.write(to_string)
