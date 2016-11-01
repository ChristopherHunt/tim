#!/usr/bin/python3

class AICore:
    'Class to define the interface for the core card choosing logic for a bot.'

    def __init__(self, name):
        self.ai_name = name

    def name(self):
        return self.ai_name
        
    def pick_card_from_pack(self, pack):
         raise NotImplementedError('pick_card_from_pack not implemented!')
