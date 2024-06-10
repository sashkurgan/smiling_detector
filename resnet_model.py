# display, transform, read, split ...
import numpy as np
import cv2 as cv
import os

import matplotlib.pyplot as plt

# tensorflow
import tensorflow as tf
from tensorflow import keras

# image processing
from keras.preprocessing import image
from keras.preprocessing.image import load_img
from keras.utils import image_dataset_from_directory

# model / neural network
from keras import layers
from keras.models import Sequential, Model
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input


image_size = (128,128)

train_dataset = image_dataset_from_directory("train", image_size=image_size)
validation_dataset = image_dataset_from_directory("validation", image_size=image_size)
# freeze resnet weights
resnet_50 = ResNet50(include_top=False, weights='imagenet', input_shape=image_size + (3,))
for layer in resnet_50.layers:
    layer.trainable = False



# build the entire model
x = resnet_50.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(512, activation='relu')(x)
x = layers.Dropout(0.5)(x)
x = layers.Dense(256, activation='relu')(x)
x = layers.Dropout(0.5)(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)
x = layers.Dense(64, activation='relu')(x)
x = layers.Dropout(0.3)(x)
predictions = layers.Dense(1, activation='sigmoid')(x)
model = Model(inputs = resnet_50.input, outputs = predictions)


# define training function
def trainModel(model, epochs, optimizer):
    batch_size = 32
    model.compile(optimizer=optimizer, loss="binary_crossentropy", metrics=["AUC"])
    return model.fit(train_dataset, validation_data=validation_dataset, epochs=epochs, batch_size=batch_size)


# launch the training
model_history = trainModel(model = model, epochs = 10, optimizer = "Adam")


model.save('smiling_detector_model_1.keras')

#plot epoch graphs
loss_train_curve = model_history.history["loss"]
loss_val_curve = model_history.history["val_loss"]
plt.plot(loss_train_curve, label = "Train")
plt.plot(loss_val_curve, label = "Validation")
plt.legend(loc = 'upper right')
plt.title("Loss")
plt.show()

