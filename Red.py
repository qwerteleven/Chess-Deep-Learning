import tensorflow as tf
from tensorflow import keras as k


def getModel():
    model = tf.keras.Sequential

    model.add(k.layers.ConvLSTM2D())

    return model


mdel = getModel()

mdel.compile()

