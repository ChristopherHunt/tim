'''
A very simple timmy bot for MTG drafting.

To Run: python3 timmy.py
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

## Import path hacking to make this run referencing the modules it needs.
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                             os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.pack_generator import PackGenerator
from lib.draft_data_reader import DraftDataReader

import argparse

import tensorflow as tf

FLAGS = None

## Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 timmy.py <training_packs.txt> <validation_packs.txt> [set_file.json] [card_rankings.txt]\n'
          '|  training_packs.txt = the file containing serialized packs for training the NN\n'
          '|  validation_packs.txt = the file containing serialized packs for validating the NN\n'
          '|  set_file.json = json filename containing the MTG cards\n'
          '|  card_rankings.txt = file containing rankings for each card\n')

def main(_):
    if (len(sys.argv) != 3 and len(sys.argv) != 5):
        print_usage()
        sys.exit()

    print('Top of main')

    training_packs_file = sys.argv[1]
    validation_packs_file = sys.argv[2]
    set_file = ''
    card_rankings_file = ''
    if (len(sys.argv) == 3):
        set_file = '../../data/kaladesh/kaladesh.json'
        card_rankings_file = '../../data/kaladesh/kaladesh_pick_order.txt'
    else:
        set_file = sys.argv[3]
        card_rankings_file = sys.argv[4]

    pack_gen = PackGenerator(set_file, card_rankings_file)

    ## Create the training data reader
    training_draft_data_reader = DraftDataReader(pack_gen)
    training_draft_data_reader.read_data(training_packs_file)

    ## Create the validation data reader
    validation_draft_data_reader = DraftDataReader(pack_gen)
    validation_draft_data_reader.read_data(validation_packs_file)

    nn_node_height = pack_gen.num_cards_in_set + 1

    ''' Create the model '''
    print('Creating the initial model')

    ## X is the input placeholder which takes in N number of packs of cards
    ## (represented as an array of nn_node_height decimal valeus). Note that the keyword
    ## None here allows us to provide any number of input arrays.
    x = tf.placeholder(tf.float32, [None, nn_node_height])

    ## W is the main mesh for the NN.
    W = tf.Variable(tf.zeros([nn_node_height, nn_node_height]))

    ## b is the bias which is applied to the output of multiplying x with W, and
    ## allows us to tweak the final values to account for things.
    b = tf.Variable(tf.zeros([nn_node_height]))

    ## This is the actual line of code which represents our initial NN
    ## computation. It takes in any number of images and converts them to guesses
    ## as to what the number actually was.
    y = tf.matmul(x, W) + b

    ''' Define loss and optimizer '''

    ## This is the set of expected values for each of the trial runs.
    y_ = tf.placeholder(tf.float32, [None, nn_node_height])

    '''
    The raw formulation of cross-entropy,

    tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.softmax(y)),
                                  reduction_indices=[1]))

    can be numerically unstable.

    So here we use tf.nn.softmax_cross_entropy_with_logits on the raw outputs of
    'y', and then average across the batch.
    '''

    print('Defining the loss function')

    ## Here we define what the loss function will be for our NN. This is
    ## important because we need some way to tell our NN how well it did with its
    ## guesses so that our back-propogation step (the optimizer) can help the NN
    ## to converge to a model which makes better guesses.
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))

    print('Defining the optimization function')

    ## This is the step that ties everything together. It takes the output of the
    ## matrix multiplication (wrapped in the cross_entropy function to define
    ## loss), and applies the gradient descent optimization routine to tweak the
    ## biases within the model.
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    ## Initilize all variables and placeholders for this training session.
    sess = tf.InteractiveSession()

    ''' Train the model '''

    print('Starting the session')

    ## Launches the training session
    tf.initialize_all_variables().run()

    print('Begin training the model')

    ## Here we are running 1000 loops on 100 randomly chosen elements from the
    ## input set. Note that training in this way saves time because choosing
    ## randomly tends to be almost as effective as training over the entire
    ## dataset (and it saves time).
    count = 0
    for _ in range(1000):
        if count % 100 == 0:
            print('Training iteration: ' + str(count))
        count += 1
        ## Grab random values from the training set
        batch_xs, batch_ys = training_draft_data_reader.next_batch(100)

        ## Run those values through the model
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    ''' Test trained model '''

    print('Test the trained model')

    ## Compare the expected and actual values for each run
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

    ## Condense the above array down into a number
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    ## Print the % correct
    batch_xs, batch_ys = validation_draft_data_reader.next_batch(100)
    print(sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys}))

if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/tmp/data',
            help='Directory for storing data')
    FLAGS = parser.parse_args()
    '''
    print('Calling app.run()')
    tf.app.run()
