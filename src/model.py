import tensorflow as tf
import numpy as np

from tensorflow.keras import layers
from tensorflow.keras.models import Model

#import config

def build_lstm(config):
    inp = layers.Input(shape=(config.MAX_SEQ_LEN,))
    x = layers.Embedding(input_dim=config.VOCAB_SIZE+1,
                         output_dim=config.EMBEDDING_DIM
                        )(inp)
    x = layers.Bidirectional(layers.LSTM(units=config.LSTM_UNITS,
                    activation='tanh',
                    dropout=config.DROP_OUT_RATE,
                    return_sequences=True
                    ))(x)
    x = layers.GlobalMaxPool1D()(x)
    x = layers.Dropout(config.DROP_OUT_RATE)(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(config.DENSE_UNITS, activation='relu')(x)
    x = layers.Dropout(config.DROP_OUT_RATE)(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(1, activation='sigmoid')(x)
    model = Model(inputs=inp, outputs=x)
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy']
                 )
    tf.keras.utils.plot_model(model, './assets/model.png')
    return model

def build_ensemble():
    """Suicide predicition model.
    Returns:
         Model
    """
    import xgboost as xgb

    model = xgb.XGBClassifier(max_depth=5,
                              n_estimators=150,
                              #objective='reg:squarederror',
                              colsample_bytree=0.9,
                              metric='auc',
                              nthread=2,
                              learning_rate=0.1,
                              random_state=77
                              )
    return model