# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 11:25:37 2020

@author: User
"""
import serial
class rasModbusCommunication:
    def __init__(self, port = '/dev/ttyUSB0', baudrate = 9600, timeout = 5):
        self.__serial = serial.Serial(port = port,\
                                      baudrate = baudrate,\
                                      bytesize = serial.EIGHTBITS,\
                                      parity = serial.PARITY_NONE,\
                                      stopbits = serial.STOPBITS_ONE,\
                                      timeout = 1000)
    
    def __del__(self):
        if ( self.__serial is not None and self.__serial.isOpen() == True ):
            self.__serial.close()
    
    def openSerial(self):
        if ( self.__serial.isOpen() == False ):
            self.__serial.open()
            
    def closeSerial(self):
        if ( self.__serial.isOpen() == True ):
            self.__serial.close()
            
    def CRCcal(self, msg):
        CRC = 0xFFFF
        CRCHi = 0xFF
        CRCLo = 0xFF
        CRCLSB = 0x00
        for i in range(0, len(msg)-2,+1):
            CRC = (CRC ^ msg[i])
            for j in range(0, 8):
                CRCLSB = (CRC & 0x0001);
                CRC = ((CRC >> 1) & 0x7FFF)
    
                if (CRCLSB == 1):
                    CRC = (CRC ^ 0xA001)
        CRCHi = ((CRC >> 8) & 0xFF)
        CRCLo = (CRC & 0xFF)
        return (CRCLo,CRCHi)
    
    #CRC Valdation
    def CRCvalid(self, resp):
        CRC = self.CRCcal(resp)
        if (CRC[0]==resp[len(resp)-2]) & (CRC[1]==resp[len(resp)-1]):
            return True
        return False
    #Modbus Function Code 03 = Read Holding Registers
    def Func03Modbus(self,slave,start,NumOfPoints):
        #Function 3 request is always 8 bytes
        message = [0 for i in range(8)] 
        Slave_Address = slave
        Function = 3
        Starting_Address = start
        Number_of_Points = NumOfPoints
    
        #index0 = Slave Address
        message[0] = Slave_Address
        #index1 = Function
        message[1] = Function
        #index2 = Starting Address Hi
        message[2] = ((Starting_Address >> 8)& 0xFF)
        #index3 = Starting Address Lo
        message[3] = (Starting_Address& 0xFF)
        #index4 = Number of Points Hi
        message[4] = ((Number_of_Points >> 8)& 0xFF)
        #index5 = Number of Points Lo
        message[5] = (Number_of_Points& 0xFF)
    
        #CRC (Cyclical Redundancy Check) Calculation
        CRC = self.CRCcal(message)
       
        #index6= CRC Lo
        message[len(message) - 2] = CRC[0]#CRCLo
        #index7 = CRC Hi
        message[len(message) - 1] = CRC[1]#CRCHi
    #    print(message)
        if self.__serial.isOpen:    
            self.__serial.write("".join(chr(h) for h in message))
            responseFunc3total = 5 + 2 * Number_of_Points
            reading = self.__serial.read(responseFunc3total)
            response = [0 for i in range(len(reading))]
            for i in range(0, len(reading)):
                response[i] = ord(reading[i])
           
            if len(response)==responseFunc3total:
                CRCok = self.CRCvalid(response)
                if CRCok & (response[0]==slave) & (response[1]==Function):
                    #Byte Count in index 3 = responseFunc3[2]
                    #Number of Registers = byte count / 2 = responseFunc3[2] / 2
                    registers = ((response[2] / 2)& 0xFF)
                    values = [0 for i in range(registers)]
                    for i in range(0, len(values)):
                        #Data Hi and Registers1 from Index3
                        values[i] = response[2 * i + 3]
                        #Move to Hi
                        values[i] <<= 8
                        #Data Lo and Registers1 from Index4
                        values[i] += response[2 * i + 4]
                        negatif = values[i]>>15
                        if negatif==1:values[i]=values[i]*-1
                    return values
        else:
            print("Serial Connection is Closed")
        return []
    
    #Modbus Function Code 04 = Read Input Registers
    def Func04Modbus(self,slave,start,NumOfPoints):
        #Function 4 request is always 8 bytes
        message = [0 for i in range(8)] 
        Slave_Address = slave
        Function = 4
        Starting_Address = start
        Number_of_Points = NumOfPoints
    
        #index0 = Slave Address
        message[0] = Slave_Address
        #index1 = Function
        message[1] = Function
        #index2 = Starting Address Hi
        message[2] = ((Starting_Address >> 8)& 0xFF)
        #index3 = Starting Address Lo
        message[3] = (Starting_Address& 0xFF)
        #index4 = Number of Points Hi
        message[4] = ((Number_of_Points >> 8)& 0xFF)
        #index5 = Number of Points Lo
        message[5] = (Number_of_Points& 0xFF)
    
        #CRC (Cyclical Redundancy Check) Calculation
        CRC = self.CRCcal(message)
       
        #index6= CRC Lo
        message[len(message) - 2] = CRC[0]#CRCLo
        #index7 = CRC Hi
        message[len(message) - 1] = CRC[1]#CRCHi
       
        if self.__serial.isOpen:       
            self.__serial.write("".join(chr(h) for h in message))
            responseFunc3total = 5 + 2 * Number_of_Points
            reading = self.__serial.read(responseFunc3total)
            response = [0 for i in range(len(reading))]
            for i in range(0, len(reading)):
                response[i] = ord(reading[i])
           
            if len(response)==responseFunc3total:
                CRCok = self.CRCvalid(response)
                if CRCok & (response[0]==slave) & (response[1]==Function):
                    #Byte Count in index 3 = responseFunc3[2]
                    #Number of Registers = byte count / 2 = responseFunc3[2] / 2
                    registers = ((response[2] / 2)& 0xFF)
                    values = [0 for i in range(registers)]
                    for i in range(0, len(values)):
                        #Data Hi and Registers1 from Index3
                        values[i] = response[2 * i + 3]
                        #Move to Hi
                        values[i] <<= 8
                        #Data Lo and Registers1 from Index4
                        values[i] += response[2 * i + 4]
                        negatif = values[i]>>15
                        if negatif==1:values[i]=values[i]*-1
                    return values
        else:
            print("Serial Connection is Closed")
        return []