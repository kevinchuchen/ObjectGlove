import serial
import time
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import csv

ser = serial.Serial('COM3', 9600)#timeout = 5
ser.flushInput()
time.sleep(3)
emp = []
val1 = []
DATASET = 150 #number of datapoints/set
FILE = "data_1_1_"
data = np.zeros(shape=(DATASET,5))
output = 0
filecount=0 #changing sample number
dataset_dict = {
    'shape': {
        0: 'Rectangular', 
        1: 'Cylinder', 
        2: 'Pyramid', 
        3: 'Sphere', 
    }
}

while True:
    while True: #determine when the button is pressed, send '1' when button pushed
        print("Push button to read data")
        startBit = ser.readline()
        if startBit == b'1\r\n':
            print("Button Pushed!")
            ser.write(b'1')
            break;

    for datapoint in range(DATASET+1):
        ser_bytes = ser.readline()
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
    filecount+=1
    
    with open(FILE+str(filecount)+'.csv','w') as f: #save data
        np.savetxt(f, data, delimiter = ',',fmt='%i')

    plt.plot(data)
    plt.ylabel('bend angle')
    plt.show()

