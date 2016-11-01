#!/usr/bin/python3

import os
import sys

## Import path hacking to make this run referencing the modules it needs.
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                             os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.dummy_ai import DummyAI
from lib.draft_generator import DraftGenerator
from lib.pack_generator import PackGenerator

## Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 random_pack_generator.py <output_file> [set_file.json] [card_rankings.txt]\n'
          '|  output_file = the file to write the random packs to\n'
          '|  set_file.json = json filename containing the MTG cards\n'
          '|  card_rankings.txt = file containing rankings for each card\n')

def main():
    if (len(sys.argv) != 2 and len(sys.argv) != 4):
        print_usage()
        sys.exit()

    output_file = sys.argv[1]
    set_file = ''
    card_rankings_file = ''
    if (len(sys.argv) == 2):
        set_file = '../../data/kaladesh/kaladesh.json'
        card_rankings_file = '../../data/kaladesh/kaladesh_pick_order.txt'
    else:
        set_file = sys.argv[2]
        card_rankings_file = sys.argv[3]

    ## Create PackGenerator for Kaladesh
    pack_gen = PackGenerator(set_file, card_rankings_file)

    ## Create a default DraftGenerator
    draft_gen = DraftGenerator()

    ## Create an AI Core for the opponents in the draft
    ai_core = DummyAI()

    ## Run a draft!
    draft_gen.draft(ai_core, pack_gen, output_file)

if __name__ == '__main__':
    main()
