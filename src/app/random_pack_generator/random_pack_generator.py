#!/usr/bin/python3

'''
This program generates a file full of serialized packs (each on a separate line)
for use in training a MTG pack NN. See the useage printout for more information
on how to run this.
'''

import os
import sys

## Import path hacking to make this run referencing the modules it needs.
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                             os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.pack_generator import PackGenerator
from lib.draft_data_reader import DraftDataReader

## Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 random_pack_generator.py <count> <output_file> [set_file.json] [card_rankings.txt]\n'
          '|  count = number of random packs to generate\n'
          '|  output_file = the file to write the random packs to\n'
          '|  set_file.json = json filename containing the MTG cards\n'
          '|  card_rankings.txt = file containing rankings for each card\n')

def main():
    if (len(sys.argv) != 3 and len(sys.argv) != 5):
        print_usage()
        sys.exit()

    count = int(sys.argv[1])
    output_file = sys.argv[2]
    set_file = ''
    card_rankings_file = ''
    if (len(sys.argv) == 3):
        set_file = '../../data/kaladesh/kaladesh.json'
        card_rankings_file = '../../data/kaladesh/kaladesh_pick_order.txt'
    else:
        set_file = sys.argv[3]
        card_rankings_file = sys.argv[4]

    ## Create PackGenerator for Kaladesh
    pack_gen = PackGenerator(set_file, card_rankings_file)

    ## Generate random packs and write them to the specified file
    pack_gen.create_random_packs_file(count, output_file)

    '''
    ## Read the generated packs back in using a DraftDataReader
    draft_data_reader = DraftDataReader(pack_gen)
    draft_data_reader.read_data(output_file)
    pack_arrays, highest_pick_arrays = draft_data_reader.next_batch(5)
    print('pack_arrays: ' + str(pack_arrays))
    print('highest_pick_arrays: ' + str(highest_pick_arrays))

    print('Generating a test booster pack:')
    pack = pack_gen.generate_pack()
    print(pack)
    print('card count: ' + str(pack.count()))
    print('highest_rank_card: ' + str(pack.highest_ranked_card))
    print('serialized_pack: ' + pack.serialize())
    pack_array, highest_pick_array = pack_gen.convert_pack_to_arrays(pack)
    print('pack_array: ' + str(pack_array))
    print('highest_pick_array: ' + str(highest_pick_array))

    ## Testing pack serialization to array
    serialized_pack = pack_gen.generate_pack().serialize()
    print('serialized_pack: ' + serialized_pack)
    pack_array, highest_pick_array =\
        pack_gen.convert_serialized_pack_to_arrays(serialized_pack)
    print('pack_array: ' + str(pack_array))
    print('highest_pick_array: ' + str(highest_pick_array))
    '''

if __name__ == '__main__':
    main()
