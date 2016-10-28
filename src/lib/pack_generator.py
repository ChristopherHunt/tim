#!/usr/bin/python3

import json
import random
import sys

from card import Card
from pack import Pack
from os.path import isfile

class PackGenerator:
    'Reads in all the card and ranking information for a given Magic the\
    Gathering Set and then generates booster packs of 15 cards.'

    ## Initializes the pack generator, expects the following:
    ##  set_json_file = the path to a json file containing all of the cards for a
    ##                  given Magic the Gathering set.
    ##  card_rankings_file = the path to a text file containing the names of all
    ##                       the cards in the set, where their order represents
    ##                       their ranking relative to one another.
    def __init__(self, set_json_file, card_rankings_file):

        self.names_to_cards = {}
        self.names_to_rankings = {}
        self.commons = []
        self.uncommons = []
        self.rares = []
        self.lands = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']

        ## Parse the card json file
        self._read_cards_from_json(set_json_file)

        ## Parse the card rankings file
        self._read_card_rankings_from_file(card_rankings_file)

    ## Reads all the cards from the input JSON and populates self.names_to_cards
    def _read_cards_from_json(self, set_json_file):

        with open(set_json_file, 'r') as cards_json_file:
            cards_json_obj = json.load(cards_json_file)
            colors = {'White' : False,
                      'Blue' : False,
                      'Black' : False,
                      'Red' : False,
                      'Green' : False,
                      'Colorless': False}

            for card in cards_json_obj:
                # Clear the color values for the new card
                for color in colors:
                    colors[color] = False

                ## Parse the card's color identity
                if 'colorIdentity' not in card:
                    colors['Colorless'] = True
                else:
                    color_id = card['colorIdentity']
                    if 'W' in color_id:
                        colors['White'] = True
                    if 'U' in color_id:
                        colors['Blue'] = True
                    if 'B' in color_id:
                        colors['Black'] = True
                    if 'R' in color_id:
                        colors['Red'] = True
                    if 'G' in color_id:
                        colors['Green'] = True
                
                ## Parse the card's rarity
                rarity = card['rarity']
                if 'Common' == rarity:
                    self.commons.append(card['name'])
                elif 'Basic Land' == rarity:
                    rarity = 'Common'
                elif 'Uncommon' == rarity:
                    self.uncommons.append(card['name'])
                else:
                    self.rares.append(card['name'])
                    rarity = 'Rare'

                ## Add the card to the dictionary
                self.names_to_cards[card['name']] =\
                    Card(card['name'], colors, rarity, card['number'])

    ## Reads the cards in from the card_ranking_file, assigning their rankings
    ## in the order they are listed in the file (with the first card listed
    ## having the highest ranking).
    def _read_card_rankings_from_file(self, card_ranking_file):

        ranking = self._file_len(card_ranking_file)
        with open(card_ranking_file, 'r') as ranking_file:
            for card in ranking_file:
                self.names_to_rankings[card] = ranking
                ranking -= 1

    ## Determine the length of the file
    def _file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    ## Creates a complete Magic the Gathering pack of cards which contains 1
    ## rare, 3 uncommons and 11 commons (includes 1 land).
    def generate_pack(self):
        cards = []

        ## Add the rare to the pack
        card_name = random.choice(self.rares)
        cards.append(self.names_to_cards[card_name])

        ## Add the three uncommons to the pack
        for i in range(0, 3):
            while any(card.name == card_name for card in cards):
                card_name = random.choice(self.uncommons)
            cards.append(self.names_to_cards[card_name])

        ## Add the 10 commons to the pack
        for i in range(0, 10):
            while any(card.name == card_name for card in cards):
                card_name = random.choice(self.commons)
            cards.append(self.names_to_cards[card_name])

        ## Add the land to the pack
        cards.append(self.names_to_cards[random.choice(self.lands)])

        return Pack(cards)

def main():
    if (len(sys.argv) != 3):
        print('Improper arguments!\n'
              'Run as python3 set_file.json card_rankings.txt')
    pack_gen = PackGenerator(sys.argv[1], sys.argv[2])
    print('Generating a test booster pack:')
    pack = pack_gen.generate_pack()
    print(pack)
    print('card count: ' + str(pack.count()))

if __name__ == '__main__':
    main()
