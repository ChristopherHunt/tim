#!/usr/bin/python3

import copy
import os
import sys
import glob

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
          '|  serialized_draft_dir = the directory containing the serialized '
                                         'draft data.\n'
          '|  output_draft_dir = the directory the results will be written to'
                                                                        '.\n'
          '|  tensor_flow_nn_filename = the file containing the Tensor Flow NN '
                                       'used for the AI\n'
          '|  set_file.json = json filename containing the MTG cards\n'
          '|  card_rankings.txt = file containing rankings for each card\n')

## Writes a list named deck to the output file specified, with each value being
## placed on a separate line. I know I should check return values but ehhhh.
def write_deck_to_file(deck, directory, file_name, name_type):
    # generate a unique filename
    # split the path to get the name from the end
    file_name = file_name.split('/')[-1]
    # get the name of the draft file
    file_name = '_'.join(file_name.split('_')[:2])
    # prepend with 'datum' or 'text'
    file_name = name_type + '_' + file_name + '.txt'
    with open(directory + file_name, 'w') as file_out:
        for card_index in deck:
          file_out.write(str(card_index) + '\n')

## Reads the contents of a file into a list and returns that list to the caller.
def read_file_into_list(filename):
    file_handle = open(filename, 'r')
    contents = []
    for line in file_handle:
      contents.append(line.strip().replace(' ', ''))
    file_handle.close()
    return copy.deepcopy(contents)

def main():
    if (len(sys.argv) != 4 and len(sys.argv) != 6):
        print_usage()
        sys.exit()

    serialized_draft_dir = sys.argv[1]
    output_dir = sys.argv[2]
    tensor_flow_nn_filename = sys.argv[3]

    # get the path names of all input files
    paths = glob.glob(serialized_draft_dir + '*.txt')

    set_file = ''
    card_rankings_file = ''
    set_file = '../../data/kaladesh/kaladesh.json'
    card_rankings_file = '../../data/kaladesh/kaladesh_pick_order.txt'
    if (len(sys.argv) == 6):
        set_file = sys.argv[4]
        card_rankings_file = sys.argv[5]

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
    for file_name in paths:
        serialized_draft_data = read_file_into_list(file_name)

        ## Run the tests!
        datum_picks, ai_picks = ai_tester.run(ai_core, serialized_draft_data)

        ## Write the datum deck (the deck that was supposed to be drafted) to disk.
        write_deck_to_file(datum_picks, output_dir, file_name, 'datum')

        ## Write the deck the ai chose to draft to disk.
        write_deck_to_file(ai_picks, output_dir, file_name, 'test')

if __name__ == '__main__':
    main()
