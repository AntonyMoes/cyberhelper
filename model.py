from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop

def get_model(maxlen, chars_num):
    model = Sequential()
    model.add(LSTM(128, input_shape=(maxlen, chars_num)))
    model.add(Dense(chars_num, activation='softmax'))

    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    return model