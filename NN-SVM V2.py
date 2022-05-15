import serial
import time
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
import os
from os.path import isfile, join
import glob
import matplotlib.image as mpimg
from sklearn.datasets import make_classification
from sklearn.metrics import plot_confusion_matrix


DATASET = 150
dataset_dict = {
    'shape': {
        0: 'D:\Studies\FYP\FYP1.5\AI\DATA\CUBOID.png', 
        1: 'D:\Studies\FYP\FYP1.5\AI\DATA\CYLINDER.png', 
        2: 'D:\Studies\FYP\FYP1.5\AI\DATA\\NOOBJ.png', 
        3: 'D:\Studies\FYP\FYP1.5\AI\DATA\SPHERE.png', 
    }
}


#serial comm
ser = serial.Serial('COM3', 9600)#timeout = 5
ser.flushInput()
time.sleep(3)

fileList = glob.glob("1_DATA COMPILED\*.csv")
x = []
y = []
#read train data
for fileName in fileList:
    with open(fileName, 'r') as f:
        data = f.readlines()
        #convert to float and list
        data = [list(map(float, i.strip().split(','))) for i in data]
    x.append(data)
        
    #get the label from filename and append it to a list
    y.append(int(fileName.split('_')[2]))


x = np.array(x)
y = np.array(y)
##print(x.shape)
x = x.reshape((800, 150*5))
#normalize X
##xmax, xmin = x.max(), x.min()
##x = (x-xmin)/(xmax-xmin)

#80% train(160 samples from each object), 20% test(40 samples from each object)
SEED = 51
X_train, X_test, Y_train, Y_test = train_test_split(x,y, test_size = 0.2, random_state = SEED,stratify = y)

#fitting data to SVM
clf = svm.SVC(kernel = 'rbf')#, probability = True)
##clf.fit(x, y)
clf.fit(X_train, Y_train)

y_pred = clf.predict(X_test)
#prediction accuracy
print("accuracy", metrics.accuracy_score(Y_test, y_pred))
print("Precision:",metrics.precision_score(Y_test, y_pred, average = None))
print("Recall:",metrics.recall_score(Y_test, y_pred, average = None))
plot_confusion_matrix(clf, X_test, Y_test)
plt.show()
def read_real_time_data(DATASET): #read data from glove
    data = np.zeros(shape=(DATASET,5))
    while True: #determine when the button is pressed, send '1' when button pushed
        print("Push button to read data")
        startBit = ser.readline()
        if startBit == b'1\r\n':
            print("Button Pushed!")
            ser.write(b'1')
            break;
    
    for datapoint in range(DATASET+1):
        ser_bytes = ser.readline()
        #print("Received: " + str(ser_bytes))
        if datapoint != 0: #ignore first read (bad data)
            #decode from bytes to str remove \r\n from end of line, and turn to list
            decode = ser_bytes.decode("utf-8")[:-2].split()
            #['sensorValue=', '142', 'sensorValue1=', '935', 'sensorValue2=', '199']
            count = 0
            for ind, val in enumerate(decode): #arrange values to array (row = trials, col= finger)
                if ind%2: #find odd no.
                    data[datapoint-1][count] = int(val)
                    count+=1
    ser.write(b'S')
    print("Stop sentinel sent!")

##    print(data)
    data = np.array(data)
    return data

while True:
    f, (ax1, ax2) = plt.subplots(1,2)
    x_rt = read_real_time_data(DATASET)
    x_rt1 = x_rt.reshape((1, 150*5))
    y_rt = clf.predict(x_rt1)
    print(y_rt)
##    y_prob = clf.predict_proba(x_rt)
##    print(y_prob)
##    print(y_realtime)
    imgLoc = dataset_dict['shape'][int(y_rt)]
    print(imgLoc)
    Y_img = mpimg.imread(imgLoc)
    ax1.plot(x_rt)
    ax1.set_title("Raw Data")
    ax2.imshow(Y_img)
    ax2.set_title("Predicted Object")
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()
