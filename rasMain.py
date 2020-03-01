# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 01:05:00 2020

@author: User
"""
from rasModbusCommunication import rasModbusCommunication
import time
import os
import numpy

phMagnification = 0.01 
salinityMagnification = 0.01
orpMagnification = 0.01

PHSLAVEADDRESS = 2
SALINITYSLAVEADDRESS = 4
ORPSLAVEADDRESS = 3
DOSLAVEADDRESS = 10
AMMONIASLAVEADDRESS = 11

def calculateAmmoniaValue(ammoniaSensorValue):
    ammoniaValue=numpy.array(ammoniaSensorValue[0:2], numpy.int16)
    ammoniaValue.dtype = numpy.float32
    print("Water Ammonia level: {}".format(float(ammoniaValue[0])))
    return ammoniaValue[0]

def calculateDOValue(doSensorValue):
    doValue=numpy.array(doSensorValue[0:2], numpy.int16)
    doValue.dtype = numpy.float32
    print("Water DO level: {}".format(float(doValue[0])))
    return doValue[0]
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
        phSensorValue = modbusObject.Func03Modbus(PHSLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
        phValue = claculatePHValue(phSensorValue)
        time.sleep(1)
        #Salinity Sensor
        salinitySensorValue = modbusObject.Func03Modbus(SALINITYSLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
        salinityValue = calculateSalinityValue(salinitySensorValue)
        time.sleep(1)
        
        #ORP Sensor
        orpSensorValue = modbusObject.Func03Modbus(ORPSLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
        orpValue = calculateOrpValue(orpSensorValue)
        time.sleep(1)
        
        #DO Sensor
        doSensorValue = modbusObject.Func03Modbus(DOSLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
        doValue = calculateDOValue(doSensorValue)
        time.sleep(1)
    #    
        #Ammonia Sensor
        ammoniaSensorValue = modbusObject.Func04Modbus(AMMONIASLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
        ammoniaValue = calculateAmmoniaValue(ammoniaSensorValue)
        
        time.sleep(10)
        os.system('clear')
        
        
    