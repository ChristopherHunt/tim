#!/usr/bin/python3

import copy
import os
import sys

## Import path hacking to make this run referencing the modules it needs.
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                             os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.ai_tester import AITester
from lib.dummy_ai import DummyAI
from lib.johnny_ai import JohnnyAI
from lib.pack_generator import PackGenerator
from lib.timmy_ai import TimmyAI

## Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 johnny_tester.py <serialized_draft_filename> '
                                          '<ai_picks_output_filename> '
                                          '<datum_picks_output_filename> '
                                          '<tensor_flow_nn_filename> '
                                          '[set_file.json] '
                                          '[card_rankings.txt]\n'
          '|  serialized_draft_filename = the file containing the serialized '
                                         'draft data.\n'
          '|  ai_picks_output_filename = the file to write the final deck of '
                                        'cards picked by the ai to.\n'
          '|  datum_picks_output_filename = the file to write the datum deck '
                                           'of cards which the ai should pick '
                                           'to.\n'
          '|  tensor_flow_nn_filename = the file containing the Tensor Flow NN '
                                       'used for the AI\n'
          '|  set_file.json = json filename containing the MTG cards\n'
          '|  card_rankings.txt = file containing rankings for each card\n')

## Writes a list named deck to the output file specified, with each value being
## placed on a separate line. I know I should check return values but ehhhh.
def write_deck_to_file(deck, filename):
    file_handle = open(filename, 'w')
    for card_index in deck:
      file_handle.write(str(card_index) + '\n')
    file_handle.close()

## Reads the contents of a file into a list and returns that list to the caller.
def read_file_into_list(filename):
    file_handle = open(filename, 'r')
    contents = []
    for line in file_handle:
      contents.append(line.strip().replace(' ', ''))
    file_handle.close()
    return copy.deepcopy(contents)

def main():
    if (len(sys.argv) != 5 and len(sys.argv) != 7):
        print_usage()
        sys.exit()

    serialized_draft_filename = sys.argv[1]
    ai_picks_output_filename = sys.argv[2]
    datum_picks_output_filename = sys.argv[3]
    tensor_flow_nn_filename = sys.argv[4]

    set_file = ''
    card_rankings_file = ''
    set_file = '../../data/kaladesh/kaladesh.json'
    card_rankings_file = '../../data/kaladesh/kaladesh_pick_order.txt'
    if (len(sys.argv) == 7):
        set_file = sys.argv[5]
        card_rankings_file = sys.argv[6]

    ## Create PackGenerator for Kaladesh
    pack_gen = PackGenerator(set_file, card_rankings_file)

    ## Create an AI Core for Johnny.
    ai_core = JohnnyAI(pack_gen, tensor_flow_nn_filename)

    ## Setup the test environment for the AI to run in.
    ai_tester = AITester(pack_gen)

    ai_picks = []
    datum_picks = []
    serialized_draft_data = []

    ## Read in the serialized_draft data.
    serialized_draft_data = read_file_into_list(serialized_draft_filename)

    ## Run the tests!
    datum_picks, ai_picks = ai_tester.run(ai_core, serialized_draft_data)

    ## Write the datum deck (the deck that was supposed to be drafted) to disk.
    write_deck_to_file(datum_picks, datum_picks_output_filename)

    ## Write the deck the ai chose to draft to disk.
    write_deck_to_file(ai_picks, ai_picks_output_filename)

if __name__ == '__main__':
    main()
