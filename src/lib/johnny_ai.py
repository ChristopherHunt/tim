#!/usr/bin/python3

import copy

from lib.ai_core import AICore
from lib.pack import Pack

import tensorflow as tf
import sys

class JohnnyAI(AICore):
    'More advanced Johnny Bot which tries to balance picking cards that are \
     powerful with cards that have synergy with the cards already picked.' 

    ## Instantiates a JohnnyAI which is backed by a card picking Tensor Flow
    ## model that is stored on disk at tensor_flow_nn_filename. Also requires
    ## the pack_generator for the set to properly serialize and deserialize
    ## packs for use in the Tensor Flow computations.
    def __init__(self, pack_generator, tensor_flow_nn_filename):
        ## Initialize the base class
        AICore.__init__(self, 'Johnny')

        ## Pack Generator used to serialize and deserialize packs.
        self.pack_gen = pack_generator

        ## Attempt to restore the Tensor Flow NN from disk.
        self._initialize_tensor_flow_nn(tensor_flow_nn_filename)

    ## Picks a card from the pack and returns it to the bot that called it.
    def pick_card_from_pack(self, deck, pack):
        pack_input = self.pack_gen.convert_pack_to_array(pack)
        fetches = [tf.nn.softmax(self.y)]
        res = self.session.run(fetches, feed_dict = {self.x: [pack_input]})

        ## The array of softmax values representing the pick preferences of each
        ## card in the set (arranged by card index).
        card_number_array = res[0][0]

        ## Remove any values in the softmax array that are cards not in the pack
        pack_softmax_array = [a * b for a, b in zip(pack_input, card_number_array)]

        ## Now, compute the synergy of the cards in the deck.
        deck_color_synergy = deck.get_color_distribution_of_playables(150)

        ## Apply this color synergy to the current softmax values to get an
        ## aggregate pick preference.
        pack_synergy_softmax_array =\
          self._apply_deck_color_synergy(copy.deepcopy(pack_softmax_array), deck_color_synergy)

        ## Now pick the highest ranked card in the pack.
        max_index = self._find_max_index(pack_synergy_softmax_array)
        card_to_pick = self.pack_gen.get_card_from_number(max_index)

        '''
        print('==============================')
        cards_by_color = {'White' : [],
                          'Blue'  : [],
                          'Black' : [],
                          'Red'   : [],
                          'Green' : [],
                          'Colorless': []}
        for temp_card in deck.cards:
          for color, value in temp_card.colors.items():
            if value == True:
              cards_by_color[color].append(temp_card.name)

        print('deck:')
        for color, temp_cards in cards_by_color.items():
          print(color + ':')
          for temp_card in temp_cards:
            print(temp_card)
          print()

        print('deck color breakdown: ')
        print(deck_color_synergy)
        print()
        print()
        for card_index in range(0, len(pack_softmax_array)):
          if pack_softmax_array[card_index] != 0.0:
            temp_card = self.pack_gen.get_card_from_number(card_index)
            power_softmax_value = pack_softmax_array[card_index]
            power_and_synergy_softmax_value = pack_synergy_softmax_array[card_index]
            print('Card: [' + str(power_softmax_value) +\
                  ' ---> ' + str(power_and_synergy_softmax_value) + '] : ' +\
                  str(temp_card.name))
        print('pick: ' + str(card_to_pick.name))
        print()
        print()
        input('next bot pick')
        '''

        ## Return the card to the calling AI bot
        pack.pick_card(card_to_pick)
        return card_to_pick

    def _apply_deck_color_synergy(self, pack_softmax_array, deck_color_synergy):
        for card_index in range(0, len(pack_softmax_array)):
          ## Get the initial softmax score for this card index.
          score = pack_softmax_array[card_index]

          ## If the card is actually in the pack.
          if score != 0:
            ## Get the card object from its card number.
            card = self.pack_gen.get_card_from_number(card_index)

            ## For each color, incorporate the synergy score.
            for color in card.colors:
              if card.colors[color] == True and color is not 'Colorless':
                score *= (1 + 50 * deck_color_synergy[color])

            ## Roll the new score into the softmax array.
            pack_softmax_array[card_index] = score

        return copy.deepcopy(pack_softmax_array)

    ## Iterates through the array, returning the index of the highest number.
    def _find_max_index(self, card_number_array):
        max_index = 0
        max_value = 0.0
        index = 0
        for value in card_number_array:
          if max_value < value:
            max_value = value
            max_index = index
          index += 1
        return max_index

    ## Attempts to restore the Tensor Flow model that was serialized to disk at
    ## tensor_flow_nn_filename, returning the result of this to the caller. If
    ## this cannot be acheived, None is returned.
    def _initialize_tensor_flow_nn(self, tensor_flow_nn_filename):
        nn_node_height = self.pack_gen.num_cards_in_set + 1

        ''' Create the model '''
        print('Creating the initial model')

        ## X is the input placeholder which takes in N number of packs of cards
        ## (represented as an array of nn_node_height decimal valeus). Note that the keyword
        ## None here allows us to provide any number of input arrays.
        self.x = tf.placeholder(tf.float32, [None, nn_node_height])

        ## W is the main mesh for the NN.
        self.W = tf.Variable(tf.zeros([nn_node_height, nn_node_height]))

        ## b is the bias which is applied to the output of multiplying x with W, and
        ## allows us to tweak the final values to account for things.
        self.b = tf.Variable(tf.zeros([nn_node_height]))

        ## This is the actual line of code which represents our initial NN
        ## computation. It takes in any number of images and converts them to guesses
        ## as to what the number actually was.
        self.y = tf.matmul(self.x, self.W) + self.b

        ''' Define loss and optimizer '''

        ## This is the set of expected values for each of the trial runs.
        self.y_ = tf.placeholder(tf.float32, [None, nn_node_height])

        print('Defining the loss function')

        ## Initilize all variables and placeholders for this training session.
        self.session = tf.InteractiveSession()

        print('Starting the session')
        self.saver = tf.train.Saver()

        ## Launches the training session
        tf.initialize_all_variables().run()

        ''' Restore the model '''
        self.saver.restore(self.session, tensor_flow_nn_filename)

        print('Model ready')
