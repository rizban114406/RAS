# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 01:05:00 2020

@author: User
"""
from rasModbusCommunication import rasModbusCommunication
import time
import os

phMagnification = 0.01 
salinityMagnification = 0.01
orpMagnification = 0.01

-35424
16606
a = -35424
print(bin(a))
0b1000101001100000
0b100000011011110
b = 16606
print(bin(b))
new = a | b >> 16
print(bin(new))
#0b11010010000000001111000
#from ast import literal_eval
#
#float_str = "0b11010010000000001111000"
#result = float(literal_eval(float_str))
#print(result)
#
#from struct import *
## Two integers to a floating point
#i1 = 0xC3F5
#i2 = 0x4840
#f = unpack('f',pack('>HH',i1,i2))[0]
#
## Floating point to two integers
#i1, i2 = unpack('>HH',pack('f',3.14))
#print(i1)
#print(i2)

def calculateDOValue(doSensorValue):
    print(doSensorValue[0])
    print(doSensorValue[1])
    doValue = doSensorValue[0] << 16 | doSensorValue[1]
    print("Water DO level: {}".format(float(doValue)))
    return doValue
#    a = 105
#    print(bin(a))

def calculateOrpValue(orpSensorValue):
    orpValue = orpSensorValue[1] * orpMagnification
    print("Water orp level: {}".format(orpValue))
    return orpValue

def calculateSalinityValue(salinitySensorValue):
    salinityValue = salinitySensorValue[3] * salinityMagnification
    print("Water salinity level: {}".format(salinityValue))
    return salinityValue

def claculatePHValue(phSensorValue):
    phValue = phSensorValue[1] * phMagnification
    print("Water PH level: {}".format(phValue))
    return phValue

if __name__ == '__main__':
    modbusObject = rasModbusCommunication()
    while 1:
        modbusObject.openSerial()
        Slave_id = 2
        Start_address = 0
        Number_of_Registers = 10
        
        #pH Sensor
        phSensorValue = modbusObject.Func03Modbus(2,Start_address,Number_of_Registers)#slave,start,number of registers
        claculatePHValue(phSensorValue)
        time.sleep(1)
#        #Salinity Sensor
#        print("Salinity Sensor Value: ")
#        salinitySensorValue = modbusObject.Func03Modbus(4,Start_address,Number_of_Registers)#slave,start,number of registers
#        print(salinitySensorValue)
#        time.sleep(1)
        
    #    #ORP Sensor
#        print("ORP Sensor Value: ")
#        orpSensorValue = modbusObject.Func03Modbus(3,Start_address,Number_of_Registers)#slave,start,number of registers
#        print(orpSensorValue)
#        time.sleep(1)
    #    
    #    DO Sensor
#        print("DO Sensor Value: ")
        doSensorValue = modbusObject.Func03Modbus(10,Start_address,Number_of_Registers)#slave,start,number of registers
        calculateDOValue(doSensorValue)
        time.sleep(1)
    #    
#        #pH Sensor
#        print("Ammonia Sensor Value: ")
#        ammoniaSensorValue = modbusObject.Func04Modbus(11,Start_address,Number_of_Registers)#slave,start,number of registers
#        print(ammoniaSensorValue)
        
        time.sleep(10)
        os.system('clear')
        
        
    