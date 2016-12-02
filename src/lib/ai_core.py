#!/usr/bin/python3

class AICore(object):
    'Class to define the interface for the core card choosing logic for a bot.'

    def __init__(self, name):
        self.ai_name = name

    ## Returns the name of the AI.
    def name(self):
        return self.ai_name
        
    ## Picks a card from a pack using the specified AI logic.
    def pick_card_from_pack(self, deck, pack):
         raise NotImplementedError('pick_card_from_pack not implemented!')
