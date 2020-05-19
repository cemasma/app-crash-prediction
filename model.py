from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
import keras
from keras.layers import Input, Dense
from keras.optimizers import SGD
import numpy as np
from init import *




A = np.array(logs_arr)

input = A[:, 0:7]
output = A[:, 7]

for i in range(0, len(output)):
    print(output[i])

model = Sequential()

model.add(Dense(256, input_dim=7))
model.add(Activation("relu"))
model.add(Dense(256))
model.add(Activation("relu"))
model.add(Dense(1))
model.add(Activation("sigmoid"))
'''
model.add(Dense(activation="sigmoid", input_dim=7, units=6, kernel_initializer="uniform"))
model.add(Dropout(p= 0.1))

model.add(Dense(activation="sigmoid", units=6, kernel_initializer="uniform"))

model.add(Dense(activation="sigmoid", units=1, kernel_initializer="uniform"))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
'''


model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(input, output, epochs=200, batch_size=50)

logs = [
    [1, 0, 1, 0, 200, 0, 71.49000000953674, 0.0],
    [1, 0, 1, 0, 200, 0, 4.077000021934509],
    [1, 0, 1, 0, 200, 0, 505.442999958992, 0.30076142131979694],
    [3, 0, 1, 2, 503, 0, 262.658999979496, 0.10659898477157363]
]

def make_predictions(logs):
    for log in logs:
        predict = np.array([log[0], log[1], log[2], log[3] , log[4], log[5], log[6]]).reshape(1, 7)
        print("Predict: " + str(model.predict_classes(predict)) + "\n\n")


print()
make_predictions(logs)