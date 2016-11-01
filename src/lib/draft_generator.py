#!/usr/bin/python3

import sys

import collections
import os

from lib.ai_core import AICore
from lib.pack_generator import PackGenerator
from lib.player import Player
from lib.ai_player import AIPlayer
from lib.human_player import HumanPlayer

class DraftGenerator:
    'Creates a draft of 7 AI\'s and a single player'

    def __init__(self):
        self.player_queue = []
        self.pack_queue = collections.deque([])

    ## Setup the draft, creating 7 AI players (all with the ai_core logic) and
    ## a single human player. The pack_generator dictates what packs are going
    ## to be created per round of the draft.
    def _build_draft(self, ai_core, pack_generator):
        ## Add the Human drafter
        self.player_queue.append(HumanPlayer('Human'))

        ## Add the AI drafters
        for x in range(1, 8):
            ai_name = ai_core.name() + '_' + str(x)
            self.player_queue.append(AIPlayer(ai_name, ai_core))

    ## Gives each seat of the table a pack.
    def _distribute_one_round_of_packs(self, pack_generator):
        ## Clear the table to start
        self.pack_queue.clear()

        ## Give each player's seat a pack to draft from
        for x in range(0, 8):
            self.pack_queue.append(pack_generator.generate_pack())

    ## Drafts a full round rotating to the left.
    def _draft_left(self, pack_generator):
        ## Give each player's seat a pack
        self._distribute_one_round_of_packs(pack_generator)

        ## Pick all cards from the packs for this round
        for pick in range(0, 15):

            ## Have each player pick a card from their pack
            for player, pack in zip(self.player_queue, self.pack_queue):
                player.pick_card_from_pack(pack)

            ## Rotate the packs amongst the players
            rotating_pack = self.pack_queue.pop()
            self.pack_queue.appendleft(rotating_pack)

        ## Remove all the empty packs from the table
        self.pack_queue.clear()

    ## Drafts a full round rotating to the right.
    def _draft_right(self, pack_generator):
        ## Give each player's seat a pack
        self._distribute_one_round_of_packs(pack_generator)

        ## Pick all cards from the packs for this round
        for pick in range(0, 15):

            ## Have each player pick a card from their pack
            for player, pack in zip(reversed(self.player_queue), self.pack_queue):
                player.pick_card_from_pack(pack)

            ## Rotate the packs amongst the players
            rotating_pack = self.pack_queue.pop()
            self.pack_queue.appendleft(rotating_pack)

        ## Remove all the empty packs from the table
        self.pack_queue.clear()

    ## Prints each player's deck information to the specified file.
    def _print_draft_results(self, output_file):
        os.remove(output_file)
        for player in self.player_queue:
            player.print_deck_to_file(output_file)

    ## Runs the draft!
    def draft(self, ai_core, pack_generator, output_file):
        ## Create all the players and give them their packs
        self._build_draft(ai_core, pack_generator)

        ## Draft the first pack
        self._draft_left(pack_generator)

        ## Draft the second pack
        self._draft_right(pack_generator)

        ## Draft the third pack
        self._draft_left(pack_generator)

        ## Print results to file
        self._print_draft_results(output_file)
