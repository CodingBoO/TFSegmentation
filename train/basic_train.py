"""
The Basic class to train any Model
"""

import tensorflow as tf

from utils.misc import timeit


class BasicTrain(object):
    """
    A Base class for train classes of the models
    Contain all necessary functions for training
    """

    def __init__(self, args, sess, model):
        print("\nTraining is initializing itself\n")

        self.args = args
        self.sess = sess
        self.model = model

        # shortcut for model params
        self.params = self.model.params

        # To initialize all variables
        self.init = None
        self.init_model()

        # Create a saver object
        self.saver = tf.train.Saver(max_to_keep=self.args.max_to_keep,
                                    keep_checkpoint_every_n_hours=10,
                                    save_relative_paths=True)

        self.saver_best = tf.train.Saver(max_to_keep=1,
                                         save_relative_paths=True)

        # Load from latest checkpoint if found
        self.load_model()

    @timeit
    def init_model(self):
        print("Initializing the variables of the model")
        self.init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        self.sess.run(self.init)
        print("Initialization finished")

    def save_model(self):
        """
        Save Model Checkpoint
        :return:
        """
        print("saving a checkpoint")
        self.saver.save(self.sess, self.args.checkpoint_dir, self.model.global_step_tensor)
        print("Saved a checkpoint")

    def save_best_model(self):
        """
        Save Model Checkpoint
        :return:
        """
        print("saving a checkpoint for the best model")
        self.saver_best.save(self.sess, self.args.checkpoint_best_dir, self.model.global_step_tensor)
        print("Saved a checkpoint for the best model")

    @timeit
    def load_model(self):
        """
        Load the latest checkpoint
        :return:
        """
        print("Searching for a checkpoint")
        latest_checkpoint = tf.train.latest_checkpoint(self.args.checkpoint_dir)
        if latest_checkpoint:
            print("Loading model checkpoint {} ...\n".format(latest_checkpoint))
            self.saver.restore(self.sess, latest_checkpoint)
            print("Model loaded from the latest checkpoint\n")
        else:
            print("\n.. No ckpt, SO First time to train :D ..\n")

    def train(self):
        raise NotImplementedError("train function is not implemented in the trainer")

    def finalize(self):
        raise NotImplementedError("finalize function is not implemented in the trainer")
