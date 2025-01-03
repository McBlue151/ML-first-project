# -*- coding: utf-8 -*-
"""Intro to AI project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wG06nSVVRcwADpv05TC8Z1u3J0SLpuPM

Using data from https://www.kaggle.com/competitions/digit-recognizer .
"""

#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Input, GlobalMaxPooling2D
from tensorflow.keras.utils import to_categorical
from keras.callbacks import ReduceLROnPlateau
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

#import datasets
from google.colab import drive
drive.mount('/content/drive')

train = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Into to AI class/train.csv')
test = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Into to AI class/test.csv')

#review size of data sets
print("Train data set size (rows, columns) is", train.shape)
print("Test data set size (rows, columns) is", test.shape)

#show train data sets top 5 rows
train.head()

#show test data sets top 5 rows
test.head()

#review data sets to see if there are any missing values
print("Train data set has", train.isnull().sum().sum(), "missing values")
print("Test data set has", test.isnull().sum().sum(), "missing values")

#count frequency of labels
train_label=train["label"]
train_label.value_counts()

#remove label column in train data set to test/validate
train=train.drop(columns='label')
train.columns

#reshape train and test models to same size of (LxWxD) 28x28x1 and normalize
X_train=train.values.reshape(train.shape[0],28,28,1)/255.0
Y_train=test.values.reshape(test.shape[0],28,28,1)/255.0

#use tensorflow and keras to build a CNN with the layers required
model=models.Sequential()

model.add(Conv2D(filters=64,kernel_size=3,padding='same',activation='relu',input_shape=(28,28,1)))
model.add(Conv2D(filters=64,kernel_size=3,padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=128,kernel_size=3,padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=128,kernel_size=3,padding='same',activation='relu'))
model.add(Conv2D(filters=192,kernel_size=3,padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=256,kernel_size=3,padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=2,padding='same'))
model.add(Flatten())
model.add(Dense(units=256,activation='relu'))
model.add(Dense(units=10,activation='softmax'))

model.summary()

#compile the model
y_train_encoded=to_categorical(train_label,num_classes=10)
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
history=model.fit(X_train,y_train_encoded,epochs=10,validation_split=0.1)

#visualize loss and accuracy of model
history_frame = pd.DataFrame(history.history)
history_frame.loc[: , ['loss', 'val_loss']].plot()
history_frame.loc[: , ['accuracy', 'val_accuracy']].plot()

#predict model
predictions=model.predict(Y_train)
predicted_labels=np.argmax(predictions,axis=1)

predictions

#create submission file for Kaggle Competition
submission=pd.DataFrame({"ImageId":range(1,len(predicted_labels)+1),"Label":predicted_labels})
submission.to_csv("submission.csv",index=False)
submission=pd.read_csv("submission.csv")
print(submission)

"""![image.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABZ4AAABkCAYAAAAG2yVGAAAgAElEQVR4Xu3daXxV1bnH8adv+rmgDL1QJ4yAAyICSqkKFKjgkEBELRomq0AYpHqFpKACMihBoQhNEFEEGZwYEkQEA8TWCW1A/ViqUEjpwCTWj4VWRnv75t48267ddfbZJznnZO+TkPPbbyTn7L32Wt+94cU/j8/6zt4/7f8/4UAAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAICCB7/zzf/9F8BwQJsMggAACCCCAAAIIIIAAAggggAACCCCAAAIIiBA88xYggAACCCCAAAIIIIAAAggggAACCCCAAAIIBCpA8BwoJ4MhgAACCCCAAAIIIIAAAggggAACCCCAAAIIEDzzDiCAAAIIIIAAAggggAACCCCAAAIIIIAAAggEKkDwHCgngyGAAAIIIIAAAggggAACCCCAAAIIIIAAAggQPPMOIIAAAggggAACCCCAAAIIIIAAAggggAACCAQqQPAcKCeDIYAAAggggAACCCCAAAIIIIAAAggggAACCBA88w4ggAACCCCAAAIIIIAAAggggAACCCCAAAIIBCpA8BwoJ4MhgAACCCCAAAIIIIAAAggggAACCCCAAAIIEDzzDiCAAAIIIIAAAggggAACCCCAAAIIIIAAAggEKkDwHCgngyGAAAIIIIAAAggggAACCCCAAAIIIIAAAggQPPMOIIAAAggggAACCCCAAAIIIIAAAggggAACCAQqQPAcKCeDIYAAAggggAACCCCAAAIIIIAAAggggAACCBA88w4ggAACCCCAAAIIIIAAAggggAACCCCAAAIIBCpA8BwoJ4MhgAACCCCAAAIIIIAAAggggAACCCCAAAIIEDzzDiCAAAIIIIAAAggggAACCCCAAAIIIIAAAggEKkDwHCgngyGAAAIIIIAAAggggAACCCCAAAIIIIAAAggQPPMOIIAAAggggAACCCCAAAIIIIAAAggggAACCAQqQPAcKCeDIYAAAggggAACCCCAAAIIIIAAAggggAACCBA88w4ggAACCCCAAAIIIIAAAggggAACCCCAAAIIBCpA8BwoJ4MhgAACCCCAAAIIIIAAAggggAACCCCAAAIIEDzzDiCAAAIIIIAAAggggAACCCCAAAIIIIAAAggEKkDwHCgngyGAAAIIIIAAAggggAAC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xXFx8Rq317JWNmtlcceOHVy2qkJiO8C2q5Dta7zVyTpwVlZft3WHCaa1annkqNHOfaurkjaV1clcYxaWbqGzrjv04Flvct2cbPnqxBH3BVp+d6Fc36ab799Db/hck9D53b3lMvylfPc+5zRqLh8+VJqOf/9ZMwIIIIAAAggggAACCCCAAAIIIIAAAqEIeDfd057I48aOdTbqmz1rttMuQw+7V7IG0kOHDnM297PDYm8PZf2ucaPG8vHHH7u9nbVFxfrX1knLVi2dcf02JOyb3UeOfX1MfllYJGVlZe667eDbbhHSqlUr6d27lxw/cVxK39jkbjroDbKTucYOxnUi2s7jirZto57FwAED3DWF8qBSPGhKgmdvu4vWzS6St/NKYi7VhM81CZ118N5FObLv6EH3PrHafKTYnNshgAACCCCAAAIIIIAAAggggAACCCBQrwRKSzfJ+PETYq6pqrBYL6qo2O1ea1cH+w3o1/rCrmqONQlvmw07/Pa7RsPo1atXStOmTd2vk7nG3nyxqofu1x/7TH5JUhI8K5C36rm6XssaPo/uflfSbTFmbp4vS8tXus+Gaucz+TVl7ggggAACCCCAAAIIIIAAAggggAACdV1AW1FMmjTZrXA289VK57lPPhlRzav9mm//Sf+oimdzjVYxr1q12q081s81CJ7yyGTp3qO7L4VeYzYktE8wFdh+12mQXFC5ieDOnbvcSzQkz76lr0wYPz4idDYnJHoNwXPIb+76T8skf+20iLuEVYHsrbDWmxbeOUNuvyoz5FUyPAIIIIAAAggggAACCCCAAAIIIIAAAuktoMHs8WPHHISMjIyY7SP8ejx75cxY7SvDa7vyuCphHXfXv4PkWCG193pzTeMmTSJ6Tsdzn0SuSac3I2UVz4rqt3lg0OGzX+ic1a63PDt4Vjo9V9aKAAIIIIAAAggggAACCCCAAAIIIIAAAgjUmkBKg+d/nD4mdyweGdF3WVdeXduNeHW87TX0Ou0n/ero5+V7DZvEOwznIYAAAggggAACCCCAAAIIIIAAAggggAACCNRAIKXBs84zVvisAfG0vvlyfZtuCS/n3b3lMmNTYVSgTeicMCUXIIAAAggggAACCCCAAAIIIIAAAggggAACNRZIefBcVfis33VocYXceXW29Ot4c5VVyhpgb/zsTVn7u1LZeXhPFAShc43fDQZA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)"""
