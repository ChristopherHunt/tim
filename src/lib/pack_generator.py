#!/usr/bin/python3

import copy
import json
import random
import sys

from lib.card import Card
from lib.pack import Pack

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
        self.num_cards_in_set = 0

        ## Parse the card rankings file
        self._read_card_rankings_from_file(card_rankings_file)

        ## Parse the card json file
        self._read_cards_from_json(set_json_file)

    ## Creates an array of of zeros with size equal to the number of cards in
    ## the MTG set that the PackGenerator is working off of. For each card in
    ## the input pack, it marks that card's index with a 1. Returns this array.
    def _create_pack_array(self, pack):
        ## Extra 1 b/c cards start numbering at 1
        pack_array = [0] * (self.num_cards_in_set + 1)

        for card in pack.cards:
            ## Mark each card in the pack with a 1
            pack_array[card.number] = 1

        return pack_array

    ## Creates an array of of zeros with size equal to the number of cards in
    ## the MTG set that the PackGenerator is working off of. It then sets the
    ## index of the card with the highest rank in the pack equal to 1.
    def _create_pack_highest_pick_array(self, pack):
        ## Extra 1 b/c cards start numbering at 1
        highest_pick_array = [0] * (self.num_cards_in_set + 1)
        highest_pick_array[pack.highest_ranked_card.number] = 1
        return highest_pick_array

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
                card_name = card['name']

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
                    self.commons.append(card_name)
                elif 'Basic Land' == rarity:
                    rarity = 'Common'
                elif 'Uncommon' == rarity:
                    self.uncommons.append(card_name)
                else:
                    self.rares.append(card_name)
                    rarity = 'Rare'

                ## Update the max card number in the set
                self.num_cards_in_set =\
                    max(self.num_cards_in_set, int(card['number']))

                ## Add the card to the dictionary
                self.names_to_cards[card_name] =\
                    Card(card_name, colors, rarity,
                    self.names_to_rankings[card_name], card['number'])

    ## Reads the cards in from the card_ranking_file, assigning their rankings
    ## in the order they are listed in the file (with the first card listed
    ## having the rank of 1).
    def _read_card_rankings_from_file(self, card_ranking_file):

        with open(card_ranking_file, 'r') as ranking_file:
            ranking = 1
            for card_name in ranking_file:
                card_name = card_name.rstrip()
                self.names_to_rankings[card_name] = ranking
                ranking += 1

    ## Generates a file full of random MTG booster packs (serialized).
    ##  count = the number of packs of each card count in the file
    ##  min_cards = the minimum number of cards in the generated pack
    ##  max_cards = the maximum number of cards in the generated pack
    ##  filename = the name of the output file containing the packs
    def create_random_packs_file(self, count, min_cards, max_cards, filename):
        with open(filename, 'w') as pack_file:
            ## For each count iteration
            for x in range(0, count): 
              ## Build a pack of each card count & write it to the output file.
              for num_cards in range(min_cards, max_cards + 1):
                pack = self.generate_pack(num_cards)
                pack_file.write(pack.serialize() + '\n')

    ## Creates an array of zeros with size equal to the number of cards in the
    ## MTG set that the PackGenerator is working off of. Then, for each card in
    ## the pack, it puts a 1 in the array at the index that corresponds to that
    ## card's number.
    def convert_pack_to_array(self, pack):
        return self._create_pack_array(pack)

    ## Creates an array of zeros with size equal to the number of cards in the
    ## MTG set that the PackGenerator is working off of. Then, for each card in
    ## the pack, it puts a 1 in the array at the index that corresponds to that
    ## card's number. It additionally creates a second array of the same size,
    ## with all zeros with a 1 in the index of the card with the highest
    ## ranking. Returns the tuple of these two arrays.
    def convert_pack_to_arrays(self, pack):
        pack_array = self._create_pack_array(pack)
        highest_pick_array = self._create_pack_highest_pick_array(pack)
        return pack_array, highest_pick_array

    ## Creates an array of zeros with size equal to the number of cards in the
    ## MTG set that the PackGenerator is working off of. Then, for each card in
    ## the pack, it puts a 1 in the array at the index that corresponds to that
    ## card's number. It additionally creates a second array of the same size,
    ## with all zeros with a 1 in the index of the card with the highest
    ## ranking. Returns the tuple of these two arrays.
    def convert_serialized_pack_to_arrays(self, serialized_pack):
        pack_list = serialized_pack.split(',')
        pack_array = [0] * (self.num_cards_in_set + 1)
        highest_pick_array = [0] * (self.num_cards_in_set + 1)

        ## Pull out the highest ranked card from the serialized pack.
        ## By convention, this is always the first card in the array.
        highest_ranked_card_num = int(pack_list[0])

        ## Set that card's index to a 1 in the pick array
        highest_pick_array[highest_ranked_card_num] = 1

        ## Set all the cards indices to 1 in the pack_array
        for card_num in pack_list[1:]:
            pack_array[int(card_num)] = 1

        return pack_array, highest_pick_array

    ## Creates a Magic the Gathering pack of cards which contains up to 1
    ## rare, 3 uncommons and 11 commons (includes 1 land). The number of cards
    ## in the pack is determined by num_cards.
    def generate_pack(self, num_cards):
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

        ## Remove cards randomly from the pack until it has num_cards in it.
        pack_size = len(cards)
        for i in range(0, pack_size - num_cards):
          cards.remove(random.choice(cards))

        return Pack(cards)

    ## Returns a Card object for the card that has the specified card_number, or
    ## None if no card exists in the current card set that this PackGenerator
    ## instance is working off of.
    def get_card_from_number(self, card_number):
        for card in self.names_to_cards.values(): 
          if card.number == card_number:
            return copy.deepcopy(card)
        return None
