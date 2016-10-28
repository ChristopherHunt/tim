## Copyright 2015 The TensorFlow Authors. All Rights Reserved.
##
## Licensed under the Apache License, Version 2.0 (the 'License');
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an 'AS IS' BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## =============================================================================

'''
A very simple MNIST classifier.

See extensive documentation at
http://tensorflow.org/tutorials/mnist/beginners/index.md

To Run: python3 mnist_softmax.py
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

## Import data
from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None

def main(_):
    print('Top of main')
    print('FLAGS.data_dir: ' + str(FLAGS.data_dir))
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

    ''' Create the model '''
    print('Creating the initial model')

    ## X is the input placeholder which takes in N number of hand-written symbols
    ## (represented as an array of 784 decimal valeus). Note that the keyword
    ## None here allows us to provide any number of input arrays.
    x = tf.placeholder(tf.float32, [None, 784])

    ## W is the main mesh for the NN, and acts as a way of condensing the input
    ## 784 decimal values down to a 10 decimal range.
    W = tf.Variable(tf.zeros([784, 10]))

    ## b is the bias which is applied to the output of multiplying x with W, and
    ## allows us to tweak the final values to account for things.
    b = tf.Variable(tf.zeros([10]))

    ## This is the actual line of code which represents our initial NN
    ## computation. It takes in any number of images and converts them to guesses
    ## as to what the number actually was.
    y = tf.matmul(x, W) + b

    ''' Define loss and optimizer '''

    ## This is a placeholder which acts as the biases to be applied to each of
    ## the output "guesses" from the above matrix multipleication. We will use
    ## this in conjunction with our defined loss and optimization functions to do
    ## back-propogation so that our NN learns.
    y_ = tf.placeholder(tf.float32, [None, 10])

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
    for _ in range(1000):
        ## Grab random values from the training set
        batch_xs, batch_ys = mnist.train.next_batch(100)

        ## Run those values through the model
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    ''' Test trained model '''

    print('Test the trained model')

    ## Compare the expected and actual values for each run
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

    ## Condense the above array down into a number
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    ## Print the % correct
    print(sess.run(accuracy, feed_dict={x: mnist.test.images,
          y_: mnist.test.labels}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/tmp/data',
            help='Directory for storing data')
    FLAGS = parser.parse_args()
    print('Calling app.run()')
    tf.app.run()
