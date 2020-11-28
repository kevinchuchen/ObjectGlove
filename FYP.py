import serial
import time
import numpy as np

ser = serial.Serial('COM3', 9600)#timeout = 5
ser.flushInput()
time.sleep(3)
emp = []
val1 = []
DATASET = 200
data = np.zeros(shape=(DATASET,3))


while True:
    while True: #determine when the button is pressed, send '1' when button pushed
        startBit = ser.readline()
        print("start: " + str(startBit))
        if startBit == b'1\r\n':
            ser.write(b'1')
            print('1 sent')
            break;

    for i in range(DATASET+1):
        ser_bytes = ser.readline()
        print("Received: " + str(ser_bytes))
        if i != 0: #ignore first read (bad data)
            #decode from bytes to str remove \r\n from end of line, and turn to list
            decode = ser_bytes.decode("utf-8")[:-2].split()
            #['sensorValue=', '142', 'sensorValue1=', '935', 'sensorValue2=', '199']
            count = 0
            for ind, val in enumerate(decode): #arrange values to array (row = trials, col= finger)
                if ind%2:
                    data[i-1][count] = int(val)
                    count+=1
    ser.write(b'S')
    print(data)

