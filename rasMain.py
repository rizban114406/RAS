# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 01:05:00 2020

@author: User
"""
from rasModbusCommunication import rasModbusCommunication
import time
import os
if __name__ == '__main__':
    modbusObject = rasModbusCommunication()  
    while 1:
        modbusObject.openSerial()
        Slave_id = 2
        Start_address = 0
        Number_of_Registers = 10
        
        #pH Sensor
        print("pH Sensor Value: ")
        phSensorValue = modbusObject.Func03Modbus(2,Start_address,Number_of_Registers)#slave,start,number of registers
        print(phSensorValue)
        time.sleep(1)
#        #Salinity Sensor
#        print("Salinity Sensor Value: ")
#        salinitySensor = modbusObject.Func03Modbus(4,Start_address,Number_of_Registers)#slave,start,number of registers
#        print(salinitySensor)
#        time.sleep(1)
        
    #    #ORP Sensor
#        print("ORP Sensor Value: ")
#        orpSensorValue = modbusObject.Func03Modbus(3,Start_address,Number_of_Registers)#slave,start,number of registers
#        print(orpSensorValue)
#        time.sleep(1)
    #    
    #    DO Sensor
        print("DO Sensor Value: ")
        doSensorValue = modbusObject.Func03Modbus(10,Start_address,Number_of_Registers)#slave,start,number of registers
        print(doSensorValue)
        time.sleep(1)
    #    
#        #pH Sensor
#        print("Ammonia Sensor Value: ")
#        ammoniaSensorValue = modbusObject.Func04Modbus(11,Start_address,Number_of_Registers)#slave,start,number of registers
#        print(ammoniaSensorValue)
        
        time.sleep(10)
        os.system('clear')
        
        
    