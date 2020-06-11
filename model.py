from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
import keras
from keras.layers import Input, Dense
from keras.optimizers import SGD
import numpy as np
from init import *




A = np.array(calculate_logs("data.jsonl"))

B = np.array(calculate_logs("testdata.jsonl"))

input = A[:, 0:7]
output = A[:, 7]

test_input = B[:, 0:7]
test_output = B[:, 7].astype(np.float)

print(test_input[0])
print(np.array(test_input[0]).reshape(1,7))

for i in range(0, len(output)):
    print(output[i])

model = Sequential()

model.add(Dense(16, input_dim=7))
model.add(Activation("sigmoid"))
model.add(Dense(8))
model.add(Activation("sigmoid"))
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
    [1, 0, 1, 0, 200, 0, 4.077000021934509, 0.0],
    [1, 0, 1, 0, 200, 0, 505.442999958992, 0.30076142131979694],
    [3, 0, 1, 2, 503, 0, 262.658999979496, 0.10659898477157363]
]

confusion_matrix = [[0, 0], [0, 0]]

def make_predictions(logs):
    for log in logs:
        predict = np.array([log[0], log[1], log[2], log[3] , log[4], log[5], log[6]]).reshape(1, 7)
        print("Predict: " + str(model.predict_classes(predict)) + "\n\n")

    print(test_input)
    for index in range(0, len(test_input)):
        ti = np.array(test_input[index]).reshape(1, 7)
        predict_result = model.predict_classes(ti)

        expected_output = 1 if test_output[index] > 0.5 else 0
        actual_output = predict_result[0][0]

        if expected_output == 1:
            if actual_output == expected_output:
                confusion_matrix[0][0] += 1
            else:
                confusion_matrix[1][0] += 1
        elif expected_output == 0:
            if actual_output == expected_output:
                confusion_matrix[1][1] += 1
            else:
                confusion_matrix[0][1] += 1

    

        print(str(predict_result) + "\t" + str(test_output[index]))


print()
make_predictions(logs)

accuracy = (confusion_matrix[0][0] + confusion_matrix[1][1]) / len(test_input)

crash_accuracy = (confusion_matrix[0][0]) / (confusion_matrix[0][0] + confusion_matrix[1][0])

precision = confusion_matrix[0][0] / (confusion_matrix[0][0] + confusion_matrix[0][1])

print("Accuracy: " + str(accuracy))
print("Crash Accuracy: " + str(crash_accuracy))
print("Precision: " + str(precision))

