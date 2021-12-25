from os import name
import tensorflow as tf
import tensorflow.keras.layers as layers

tf.random.uniform

class Proposed(tf.keras.Model):
    def __init__(self, layer_size=128):
        super(Proposed, self).__init__()
        self.encoder1 = layers.LSTM(layer_size,
                                    return_state=True, 
                                    return_sequences=True, 
                                    name='encoder1')
        self.encoder2 = layers.LSTM(layer_size, 
                                    return_state=True, 
                                    return_sequences=True, 
                                    name='encoder2')
        self.attention = layers.Attention(name='attention')
        self.decoder = layers.LSTM(layer_size * 2, 
                                   return_sequences=True, 
                                   name='decoder')
        self.activation = layers.LeakyReLU(alpha=0.1)
        self.fc = layers.Dense(1, name='fc')
        
    def call(self, inputs):
        flu_inputs, web_past_inputs, web_future_inputs = inputs
        enc1_outputs, enc1_h, enc1_c = self.encoder1(flu_inputs)
        enc2_outputs, enc2_h, enc2_c = self.encoder2(web_past_inputs)
        enc_outputs = tf.concat([enc1_outputs, enc2_outputs], 
                                 axis=-1)
        enc_states = [tf.concat([enc1_h, enc2_h], axis=-1),
                      tf.concat([enc1_c, enc2_c], axis=-1)]
        
        dec_outputs = self.decoder(web_future_inputs,
                                   initial_state=enc_states)
        outputs = self.attention([dec_outputs, enc_outputs])
        outputs = self.activation(outputs)
        outputs = self.fc(outputs)
        
        return outputs
        