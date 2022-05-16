try:
    USB_PORT = "/dev/ttyUSB0"
except:
    USB_PORT = "/dev/ttyUSB1"
    
#USB_PORT = "/dev/ttyACM0"  # Arduino Uno WiFi Rev2
# Imports
from datetime import datetime
import serial
import time
import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")
# Functions
# Main
# Connect to USB serial port at 9600 baud
try:
   usb = serial.Serial(USB_PORT, 2000000, timeout=2)
except:
   print("ERROR - Could not open USB serial port.  Please check your port name and permissions.")
   print("Exiting program.")
   exit()
   
dictname = {0:'No Disturbance', 1: 'Sag', 2: 'Swell', 3: 'Interruption', 4:'Harmonic', 5:'Flicker', 6:'Transient',7:'Sag + Harmonic',8:'Swell + Harmonic',9:'Flicker + Harmonic',10:'Flicker + Sag',11:'Flicker + Swell',12:'Flicker + Transient',13:'Flicker + Sag +Harmonic',14:'Flicker +Swell + Harmonic'}
model = tf.keras.models.load_model('model_rpi')
trans = MinMaxScaler((-1,1))
def givenum(ar):
    for i in range(len(ar)):
        if i==1:
            count=i        
        else:
            count=0
    return count
# Send commands to Arduino
while True:
    li=[]
    print("Input begins  now - ")
    time.sleep(2)
    while len(li)<201:
        
        
       # read Arduino A0 pin value  # send command to Arduino
        line = usb.readline()  # read input from Arduino
        line = line.decode()  # convert type from bytes to string
        line = line.strip()  # strip extra whitespace characters
        if line.isdigit():  # check if line contains only digits
            value = int(line)  # convert type from string to int
            #if len(li)<200:
            li.append(value)
        else:
            
            print("Unknown value" + line + "', setting to 0.")
            
        #print("Arduino A0 value:", value)
    
    print(li,'\n')
    sigtest = np.reshape(li[1:], (1,200,1))
    testsig2= np.array(sigtest)
    for i in range(len(sigtest)):
        testsig2[i] = trans.fit_transform(sigtest[i])
    now = datetime.now()
    ct=now.strftime("%H:%M:%S")    
    print("The Model's prediction at time =",ct," is - ",dictname[givenum(model.predict(testsig2))])
    print('\n')
