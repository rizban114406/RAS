# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 01:05:00 2020

@author: User
"""
from rasModbusCommunication import rasModbusCommunication
import time
import os
import numpy
from rasLCD import rasLCD
rasLCDObject = rasLCD()

phMagnification = 0.01 
salinityMagnification = 0.01
orpMagnification = 0.01
tempMagnification = 0.1

PHSLAVEADDRESS = 2
SALINITYSLAVEADDRESS = 4
ORPSLAVEADDRESS = 3
DOSLAVEADDRESS = 10
AMMONIASLAVEADDRESS = 11

def calculateAmmoniaValue(ammoniaSensorValue):
    if (len(ammoniaSensorValue) > 0):
        ammoniaValue=numpy.array(ammoniaSensorValue[0:2], numpy.int16)
        ammoniaValue.dtype = numpy.float32        
        tempValue = ammoniaSensorValue[3] * tempMagnification
        return ammoniaValue[0],tempValue
    return "NA","NA"

def calculateDOValue(doSensorValue):
    if (len(doSensorValue) > 0):
        doValue=numpy.array(doSensorValue[0:2], numpy.int16)
        doValue.dtype = numpy.float32
        return doValue[0]
    return "NA"
#    a = 105
#    print(bin(a))

def calculateOrpValue(orpSensorValue):
    if (len(orpSensorValue) > 0):
        orpValue = orpSensorValue[1]
        return int(orpValue)
    return "NA"

def calculateSalinityValue(salinitySensorValue):
    if (len(salinitySensorValue) > 0):
        salinityValue = salinitySensorValue[3] * salinityMagnification
        return salinityValue
    return "NA"

def claculatePHValue(phSensorValue):
    if (len(phSensorValue) > 0):
        phValue = phSensorValue[1] * phMagnification
        return phValue
    return "NA"

if __name__ == '__main__':
    rasLCDObject.printInitialMessage()
    modbusObject = rasModbusCommunication()
    rasLCDObject.printPleaseWait()
    while 1:
        try:
            modbusObject.openSerial()
            Start_address = 0
            Number_of_Registers = 10
            
            #pH Sensor
            phSensorValue = modbusObject.Func03Modbus(PHSLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
            phValue = claculatePHValue(phSensorValue)
            if phValue != "NA":
                phValue = round(phValue,2)
            print("Water PH level: {}".format(phValue))
            time.sleep(.5)
            
            #Salinity Sensor
            salinitySensorValue = modbusObject.Func03Modbus(SALINITYSLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
            salinityValue = calculateSalinityValue(salinitySensorValue)
            if salinityValue != "NA":
                salinityValue = round(salinityValue,2)           
            print("Water salinity level: {}".format(salinityValue))
            time.sleep(.5)
            
            #ORP Sensor
            orpSensorValue = modbusObject.Func03Modbus(ORPSLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
            orpValue = calculateOrpValue(orpSensorValue)          
            print("Water orp level: {}".format(orpValue))
            time.sleep(.5)
            
            #DO Sensor
            doSensorValue = modbusObject.Func03Modbus(DOSLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
            doValue = calculateDOValue(doSensorValue)
            if doValue != "NA":
                doValue = round(doValue,2)
            print("Water DO level: {}".format(doValue))
            time.sleep(.5)
        #    
            #Ammonia Sensor
            ammoniaSensorValue = modbusObject.Func04Modbus(AMMONIASLAVEADDRESS,Start_address,Number_of_Registers)#slave,start,number of registers
            ammoniaValue,tempValue = calculateAmmoniaValue(ammoniaSensorValue)
            if ammoniaValue != "NA":
                ammoniaValue = round(ammoniaValue,2)       
            print("Water Ammonia level: {}".format(ammoniaValue))
            print("Water Temperature level: {}".format(tempValue))
            
            rasLCDObject.printDeviceData(str(phValue),str(doValue),str(salinityValue),str(orpValue),str(ammoniaValue),str(tempValue))
            time.sleep(10)
            os.system('clear')
        except Exception as e:
            print("Exception Message: {}".format(e))
        
        
    