#!/usr/bin/python3

import copy
import random
import sys

from lib.card import Card
from lib.pack import Pack
from lib.pack_generator import PackGenerator

class DraftDataReader:
    'Reads in serialized MTG draft packs and turns them into arrays which a\
    TensorFlow application could use.'

    def __init__(self, pack_generator):
        self.pack_generator = pack_generator
        self.serialized_packs = []
        
    ## Reads a file full of serialized packs into main memory.
    def read_data(self, filename):
        ## Read all the packs into main memory
        with open(filename, 'r') as pack_file:
            for serialized_pack in pack_file:
                self.serialized_packs.append(serialized_pack)

    ## Selects count number of random packs from the input file's contents and
    ## generates a pack_array and a highest_pick_array for each. These arrays
    ## are appended to their respective output lists at the same index and
    ## returned to the caller.
    def next_batch(self, count):
        pack_arrays = []
        highest_pick_arrays = []
        for n in range(0, count):
            serialized_pack = random.choice(self.serialized_packs)        
            pack_array, highest_pick_array =\
                self.pack_generator.convert_serialized_pack_to_arrays(serialized_pack)

            pack_arrays.append(copy.copy(pack_array))
            highest_pick_arrays.append(copy.copy(highest_pick_array))

        return pack_arrays, highest_pick_arrays


