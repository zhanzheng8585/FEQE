import tensorflow as tf
from tensorlayer.layers.core import Layer
from tensorlayer.decorators import private_method

class DeSubpixelConv2d(Layer):
    def __init__(self, prev_layer, scale=2, act=None, name='desubpixel_conv2d'):
        super(DeSubpixelConv2d, self).__init__(prev_layer=prev_layer, act=act, name=name)
        # Assume the input have desired shape
        
        if int(self.inputs.get_shape()[-2]) % scale != 0 or int(self.inputs.get_shape()[-3]) % scale != 0:
            raise Exception('input width and height should be devided by scale of', scale)

        with tf.variable_scope(name):
            self.outputs = self._apply_activation(self._PDS(self.inputs, r=scale))
        
        self._add_layers(self.outputs)

    @private_method
    def _PDS(self, X, r):
        X = tf.space_to_depth(X, r)
        return X