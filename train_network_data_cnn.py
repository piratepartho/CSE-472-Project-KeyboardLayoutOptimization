
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

punct = False

path_str = ""
num_of_epochs = 200
num_of_characters = 26
num_of_keyboards = 1000

data_file_path = "data.txt"
features = np.zeros([num_of_keyboards, num_of_characters, num_of_characters], dtype=int)
labels = np.zeros([num_of_keyboards], dtype=float)

print("loading data...")
with open(data_file_path, 'r') as data_file:
    for f in range(num_of_keyboards):
        line = data_file.readline()
        values = line.split(' ')

        for i in range(num_of_characters):
            for j in range(num_of_characters):
                features[f][i][j] = int(values[num_of_characters*i+j])

        labels[f] = float(values[-1])


print("training...")
split_point = int(0.8*num_of_keyboards)
x_train = features[:split_point]
x_test = features[split_point:]
y_train = labels[:split_point]
y_test = labels[split_point:]

model = models.Sequential()

model.add(layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(num_of_characters, num_of_characters, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(filters=128, kernel_size=(3, 3), activation='relu'))

model.add(layers.Flatten())

model.add(layers.Dense(64, activation='relu'))

model.add(layers.Dense(1)) 

model.summary()

model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['mean_absolute_error'])


history = model.fit(x_train, y_train, epochs=num_of_epochs, validation_split=0.2)


model.save('saved_model/my_model_cnn' + path_str)

print("testing...")
model.evaluate(x_test, y_test, verbose=2)
