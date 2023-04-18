import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import filedialog

# define a function to get the folder name from the user using a GUI
def get_folder_name():
    root = tk.Tk()
    root.withdraw()
    folder_name = filedialog.askdirectory()
    return folder_name

# set the number of photos to capture
n = 10

# get the folder name from the user using a GUI
dir_name = get_folder_name()

# ask the user to name the file
filename = input('Enter a filename for the photos: ')

# create a directory to store the photos
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

# initialize the webcam
cap = cv2.VideoCapture(0)

# capture n photos
for i in range(n):
    # read a frame from the webcam
    ret, frame = cap.read()

    # show the current photo
    cv2.imshow('Photo', frame)

    # save the photo to the directory with a unique filename
    file_path = os.path.join(dir_name, f'{filename}{i}.jpg')
    cv2.imwrite(file_path, frame)

    # wait for a key press to capture the next photo
    cv2.waitKey(0)

# release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()

# load the photos and their labels
X = []
y = []
for i in range(n):
    file_path = os.path.join(dir_name, f'{filename}{i}.jpg')
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    X.append(gray.flatten())
    y.append(i)

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# train a support vector machine classifier
clf = SVC()
clf.fit(X_train, y_train)
