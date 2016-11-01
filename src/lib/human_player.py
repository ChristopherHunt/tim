#!/usr/bin/python3

import copy

from lib.player import Player

class HumanPlayer(Player):
    'Class to define a human player for a Magic the Gathering draft.'

    def __init__(self, player_name):
        Player.__init__(self, player_name)

    ## Gets the user's choice of card index from stdin, and keeps looping until 
    ## a valid index is chosen
    def _get_user_card_choice(self, pack_count):
        good_choice = False

        card_index = None

        while good_choice == False:
            card_index = input('Choose a card number to pick: ')

            try:
                card_index = int(float(card_index))
                if card_index <= pack_count and card_index >= 0:
                    good_choice = True
                else:
                    raise ValueError
            except ValueError:
                print('Invalid input, choose an index between 0 and ' +
                       str(pack_count))

        return card_index

    ## Prompts the user to make a pick from the current pack. The pack's
    ## contents are displayed on screen and the user picks a card by entering
    ## the number associated with that card. Once a card is picked it is added
    ## to the player's deck and removed from the pack it was taken out of.
    def pick_card_from_pack(self, pack):
        print('\n\nPack Contents:\n')
        print('--------------\n')

        ## Display all the cards to stdout
        for i in range(0, len(pack.cards)):
            card = pack.get_card_at_index(i)
            print(str(i) + '. ' + card.name)
             
        ## Allow the user to choose a card by index         
        card_index = self._get_user_card_choice(pack.count())

        ## Add that card to the player's deck while removing it from the pack
        self.deck.add_card(copy.copy(pack.pick_card(card)))
