import os
import pickle
import numpy as np
import pandas as pd

from random import shuffle
from PIL import Image
from numpy import ndarray
from scipy import linalg, stats
from typing import List, Tuple

combined_directory = "./AllChars/"
directory_n_1 = "./recognition/batch2/"
directory_n_2 = "./recognition/batch3/"


# Takes a directory path and returns all the names of the subdirectories or images, and their paths
def open_directory(directory_path, images: bool):
    names = os.listdir(directory_path)
    if images:
        paths = [directory_path + name for name in names]
    else:
        paths = [directory_path + name + "/" for name in names]
    return paths, names


# Takes a list of image paths and returns a list of image np arrays
def open_images(image_paths):
    image_arrays = [np.array(Image.open(image_path))
                    for image_path in image_paths]
    return image_arrays


# Takes a list of image np.arrays and turns them into a large feature vector array where rows correnspond to images and columns correspond to features (pixels) of the image
def images_to_feature_vectors(images):
    h, w = images[0].shape
    n_features = h * w
    fvectors = np.empty((len(images), n_features))
    for i, image in enumerate(images):
        fvectors[i, :] = image.reshape(1, n_features)
    return fvectors


# Splits an image list into training and testing data
def split_two(image_list, ratio=[0.7, 0.3]):
    train_ratio = ratio[0]
    indices_for_splittin = [int(len(image_list) * train_ratio)]
    train, test = np.split(image_list, indices_for_splittin)
    return train, test


# Splits an image list into training, validation and testing data
def split_three(image_list, ratio=[0.8, 0.1, 0.1]):
    train_r, val_r, test_r = ratio
    assert (np.sum(ratio) == 1.0)
    indicies_for_splitting = [
        int(len(image_list) * train_r), int(len(image_list) * (train_r + val_r))]
    train, val, test = np.split(image_list, indicies_for_splitting)
    return train, val, test


# Takes the path of a directory where every image is placed into a directory with the name of the label
# and returns a dictionary with the feature vectors and their corresponding labels
def label_data(directory):
    data_labelled = {}
    data_fvectors = []
    data_labels = []
    subdirectory_paths, subdirectory_names = open_directory(
        directory, images=False)
    for i in range(len(subdirectory_names)):
        images = os.listdir(subdirectory_paths[i])
        images = [subdirectory_paths[i] + "/" + image for image in images]
        images = open_images(images)
        data_fv = images_to_feature_vectors(images)
        for fv in data_fv:
            data_fvectors.append(fv)
            data_labels.append(subdirectory_names[i])
    data_labelled["fvectors"] = data_fvectors
    data_labelled["labels"] = data_labels

    return data_labelled


# Does the same as label_data but it also splits the images into training and testing and returns seperate dictionaries
def split_train_test(directory):
    train_model = {}
    train_fvectors = []
    train_labels = []
    test_model = {}
    test_fvectors = []
    test_labels = []
    subdirectory_paths, subdirectory_names = open_directory(
        directory, images=False)
    for i in range(len(subdirectory_names)):
        images = os.listdir(subdirectory_paths[i])
        shuffle(images)
        images = [subdirectory_paths[i] + "/" + image for image in images]
        train, test = split_two(images)
        train = open_images(train)
        train_fv = images_to_feature_vectors(train)
        for fv in train_fv:
            train_fvectors.append(fv)
            train_labels.append(subdirectory_names[i])
        test = open_images(test)
        test_fv = images_to_feature_vectors(test)
        for fv in test_fv:
            test_fvectors.append(fv)
            test_labels.append(subdirectory_names[i])
    train_model["fvectors"] = train_fvectors
    train_model["labels"] = train_labels
    test_model["fvectors"] = test_fvectors
    test_model["labels"] = test_labels

    return train_model, test_model


# Save the training model to a pickle file
def save_pickle(data: dict) -> None:
    a_file = open("data.pkl", "wb")
    pickle.dump(data, a_file)
    a_file.close()


# Loads the training model from the pickle file
def load_pickle() -> dict:
    a_file = open("data.pkl", "rb")
    model = pickle.load(a_file)
    return model


# Computes the cosine similarity between arrays of training and testing data and returns the distance where rows correspond to test images and columns correspond to train images, very quick
def cosine_similarity(training, testing):
    tdott = np.dot(testing, training.transpose())
    modtrain = np.sqrt(np.sum(training * training, axis=1))
    modtest = np.sqrt(np.sum(testing * testing, axis=1))
    dist = -tdott / np.outer(modtest, modtrain.transpose())
    return dist


# computes the euclidean distance between arrays of training and testing data, pretty slow
def euclidean_distance(training, testing):
    dist = np.full([len(testing), len(training)], 0)
    for testrow in range(0, testing.shape[0]):
        for trainrow in range(0, training.shape[0]):
            dist[testrow][trainrow] = np.linalg.norm(
                testing[testrow] - training[trainrow])
    return dist


KNNC = 5  # K in K nearest neighbours


# Takes a training dict and a testing dict, computes the distance between the feature vectors, finds the k nearest images, extracts their labels,
# finds the most common label, and classifies it as such. Returns labels in the same order as the test feature vectors
def classify(train_model: dict, test_fvectors, k) -> List[str]:
    train_fvectors = np.array(train_model["fvectors"])
    train_labels = train_model["labels"]

    # Compute distance
    dist = cosine_similarity(train_fvectors, test_fvectors)

    # Extract k nearest images
    knearest = np.argsort(dist, axis=1)[:, 0:k]

    # Extract the labels of the k nearest neighbours for each test image
    klabels = [[train_labels[knearest[i][j]]
                for j in range(k)] for i in range(len(knearest))]

    # Find the most comon label and classify
    klabels = pd.DataFrame(klabels)
    labels = klabels.mode(axis='columns')
    label = np.array(labels[0].tolist())
    return label


# Computes the accuracy of the model by running classify and checking the percentage of true labels
def evaluate(train_model: dict, test: dict, k) -> Tuple[float, float]:
    true_labels = test["labels"]
    test_fvectors = np.array(test["fvectors"])
    output_labels = classify(train_model, test_fvectors, k)
    n_of_correct_labels = 0
    for i in range(len(true_labels)):
        if output_labels[i] == true_labels[i]:
            n_of_correct_labels += 1
    score = 100.0 * n_of_correct_labels / len(true_labels)
    return score


# Creates a random test/train split and runs the classifier once
def test_one(directory_of_images, k):
    train, test = split_train_test(directory_of_images)
    return evaluate(train, test, k)


# Runs the classifier n times, each time creating a new training/testing split, then prints the average accuracy of the n runs
def test_n_times(directory_of_images, k, n):
    accuracy = []
    for i in range(n):
        accuracy.append(test_one(directory_of_images, k))
    average = sum(accuracy) / n
    final_score = "Average score for k=" + \
        str(k) + " = " + str(round(average, 2))
    print(final_score)


# Saves the model using train data directory
def save_model(train_data_directory):
    model = label_data(train_data_directory)
    save_pickle(model)


# save_model(combined_directory)


# Takes the directory path of the images we want to classify and returns the corresponding labels
def classify_unlabelled_directory(segmented_image_directory):
    image_paths, _ = open_directory(segmented_image_directory, images=True)
    image_arrays = open_images(image_paths)
    image_fvectors = images_to_feature_vectors(image_arrays)
    train_model = load_pickle()
    labels = classify(train_model, image_fvectors, 3)
    return labels


def classify_image_arrays(image_arrays):
    image_fv = images_to_feature_vectors(image_arrays)
    train_model = load_pickle()
    labels = classify(train_model, image_fv, 3)
    return labels


def mapChars(listOfChars):
    mappings = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9"
    }

    finalChar = []
    for char in listOfChars:
        finalChar.append(mappings[char])
    return "".join(list((finalChar)))


# save_model(combined_directory)
# predicted_chars = classify_unlabelled_directory('./test/')
# print(predictChars(predicted_chars))
