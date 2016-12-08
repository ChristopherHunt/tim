#!/usr/bin/python3

import copy
import json
import os
import sys
import glob

## Import path hacking to make this run referencing the modules it needs.
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                             os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.ai_validator import AIValidator
from lib.dummy_ai import DummyAI
from lib.johnny_ai import JohnnyAI
from lib.pack_generator import PackGenerator
from lib.timmy_ai import TimmyAI

## Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 validator_runner.py <output_filename> '
                                             '<ai_picks_filename> '
                                             '<datum_picks_filename> '
                                             '[set_file.json] '
                                             '[card_rankings.txt]\n'
          '|  output_filename = the file to write the json output to.\n'
          '|  ai_picks_dir = the dir to write the final deck of '
                                 'cards picked by the ai to.\n'
          '|  datum_picks_dir = the dir to write the datum deck '
                                     'of cards which the ai should pick to.\n'
          '|  set_file.json = json filename containing the MTG cards\n'
          '|  card_rankings.txt = file containing rankings for each card\n')

## Reads the contents of a file into a list and returns that list to the caller.
def read_file_into_list(filename):
    file_handle = open(filename, 'r')
    contents = []
    for line in file_handle:
      contents.append(line.strip())
    file_handle.close()
    return copy.deepcopy(contents)

def write_json_to_file(dictionary, filename):
  with open(filename, 'w') as output:
    json.dump(dictionary, output)

def main():
    if (len(sys.argv) != 4 and len(sys.argv) != 6):
        print_usage()
        sys.exit()

    output_filename = sys.argv[1]
    ai_picks_dir = sys.argv[2]
    datum_picks_dir = sys.argv[3]

    # generate all paths for the ai files
    ai_paths = glob.glob(ai_picks_dir + '*.txt')
    ai_paths.sort()
    # generate all paths for the datum picks
    datum_paths = glob.glob(datum_picks_dir + '*.txt')
    datum_paths.sort()

    # zip the files together based on name
    zipped_files = zip(datum_paths, ai_paths)

    # for (d,a) in zipped_files:
        # print (d, a)
        # input()

    set_file = ''
    card_rankings_file = ''
    set_file = '../../data/kaladesh/kaladesh.json'
    card_rankings_file = '../../data/kaladesh/kaladesh_pick_order.txt'
    if (len(sys.argv) == 6):
        set_file = sys.argv[4]
        card_rankings_file = sys.argv[5]

    ## Create PackGenerator for Kaladesh
    pack_gen = PackGenerator(set_file, card_rankings_file)

    ## Setup the validation environment
    ai_validator = AIValidator(pack_gen)

    results = []
    for (datum_file, ai_file) in zipped_files:
        ## Read in the datum deck
        datum_deck = read_file_into_list(datum_file)

        ## Read in the AI's deck
        ai_deck = read_file_into_list(ai_file)

        ## Run the validation!
        results.append(ai_validator.run(datum_deck, ai_deck))

    # calculate the average values for card and color. and output to file.
    total_len = len(results)
    card = 0
    color = 0
    for d in results:
        card += d['card_similarity']
        color += d['color_dissimilarity']

    print ('card similarity ', card / total_len)
    print ('color similarity ', 1 - (color / total_len))
    # print (results)
    # input()

    ## Write the datum deck (the deck that was supposed to be drafted) to disk.
    # write_json_to_file(results, output_filename)

if __name__ == '__main__':
    main()
