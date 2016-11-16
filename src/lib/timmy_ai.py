#!/usr/bin/python3

from lib.ai_core import AICore
from lib.pack import Pack

import tensorflow as tf
import sys

class TimmyAI(AICore):
    'Simple Timmy Bot which always picks the strongest card out of a pack.'

    ## Instantiates a TimmyAI which is backed by a card picking Tensor Flow
    ## model that is stored on disk at tensor_flow_nn_filename. Also requires
    ## the pack_generator for the set to properly serialize and deserialize
    ## packs for use in the Tensor Flow computations.
    def __init__(self, pack_generator, tensor_flow_nn_filename):
        ## Initialize the base class
        AICore.__init__(self, 'Timmy')

        ## Pack Generator used to serialize and deserialize packs.
        self.pack_gen = pack_generator

        ## Attempt to restore the Tensor Flow NN from disk.
        self._initialize_tensor_flow_nn(tensor_flow_nn_filename)

    ## Picks a card from the pack and returns it to the bot that called it.
    def pick_card_from_pack(self, pack):
        pack_input = self.pack_gen.convert_pack_to_array(pack)
        fetches = [tf.nn.softmax(self.y)]
        res = self.session.run(fetches, feed_dict = {self.x: [pack_input]})
        card_number_array = res[0][0]

        ## Find the card which the Bot would ideally like to pick from the pack.
        max_index = self._find_max_index(card_number_array)
        card = self.pack_gen.get_card_from_number(max_index)

        ## Loop until the Bot picks a card. This loop is needed because the Bot
        ## might try to pick a card which isn't in the pack. So when that
        ## happens, that card's ranking is set to 0 and the next highest choice
        ## is read out from the array.
        while pack.has_card(card) == False:
          card_number_array[max_index] = 0.0
          max_index = self._find_max_index(card_number_array)
          card = self.pack_gen.get_card_from_number(max_index)

        ## Return the card to the calling AI bot
        pack.pick_card(card)
        return card

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
