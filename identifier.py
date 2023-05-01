import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import pptx
from pptx.util import Inches
import csv
from PIL import Image
import json
from bs4 import BeautifulSoup as BS
import requests
from sklearn.model_selection import train_test_split

import value_getter

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43

train_directory = "plantnet_300K/images_train"
test_directory = "plantnet_300K/images_test"
map_file = "plantnet_300K/plantnet300K_species_names.json"
model_name = "model"
csvDir = "output.csv"
id_dir = "id_dir"

def textToBool(inp):
    return inp in ["True", "true"]

def main():
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python main.py (bool)train_model")

    if (textToBool(sys.argv[1])):
        train_images, train_labels = load_data(train_directory, True)
        test_images, test_labels = load_data(test_directory)

        train_labels = tf.keras.utils.to_categorical(test_labels)

        # Get a compiled neural network
        model = get_model()

            # Fit model on training data
        for batchTrain, batchLabel in train_images, trainLabels:
            batchLabel = tf.keras.utils.to_categorical(batchLabel)
            model.fit(batchTrain, batchLabel, epochs=2)

        # images, labels = load_data("gtsrb", false)

        # # Split data into training and testing sets
        # labels = tf.keras.utils.to_categorical(labels)
        # x_train, x_test, y_train, y_test = train_test_split(
        #     np.array(images), np.array(labels), test_size=TEST_SIZE
        # )

        # Fit model on training data
        # model.fit(x_train, y_train, epochs=EPOCHS)

        # Evaluate neural network performance
        model.evaluate(test_images,  test_labels, verbose=2)

        model.save(model_name)
        print(f"Model saved to {model_name}.")
    else:
        model = tf.keras.models.load_model(model_name)
        value_getter.produce_output(model)

def splitDataFrameIntoSmaller(df, chunkSize = 10): #10 for default 
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])
    return listOfDf

def load_data(data_dir, splitBatch):
    images = []
    labels = []
    gtsrb = os.listdir(data_dir)
    for folder in gtsrb:
      if not folder.startswith("."):
        path = os.path.join(data_dir, folder)
        for image in os.listdir(path):
            imgPath = os.path.join(path, image)

            if imgPath[:-4] != ".ppm":
                im = Image.open(imgPath)
                ppmPath = f"{imgPath}.ppm"
                im.convert("RGB").save(ppmPath, "PPM")
                os.remove(imgPath)
                imgPath = ppmPath
            img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            images.append(img)
            labels.append(int(folder))

    if splitBatch:
        images = splitDataFrameIntoSmaller(images, chunkSize = 3)
        labels = splitDataFrameIntoSmaller(labels, chunkSize = 3)
    return images, labels

def get_model():
    model = tf.keras.models.Sequential(
      [
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(3, 3)),
        tf.keras.layers.Flatten(),
        #relu, sigmoid, softmax

        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(NUM_CATEGORIES * 16, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(NUM_CATEGORIES * 8, activation="relu"),

        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
      ]
    )

    model.compile(
      optimizer="adam",
      loss="binary_crossentropy",
      metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()