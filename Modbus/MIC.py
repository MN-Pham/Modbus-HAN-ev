import struct
import crcmod
import serial
import RPi.GPIO as GPIO
from time import sleep

#This library is made for reading MIC/MIC2 energy meter with a MAX485 module

#UART configuration
#8-bit data, no parity, 1 stop bit, 19200 BAUD
ser = serial.Serial("/dev/ttyS0", 38400)

#return code:
CRC_error   = -2
Trans_error = -1
No_error    = 0

class MIC2:
    def __init__(self, Id, Control):
        self.__Control = Control
        self.__Address = Id
        self.__V1 = 0
        self.__V2 = 0
        self.__V3 = 0
        self.__I1 = 0
        self.__I2 = 0
        self.__I3 = 0
        self.__P1 = 0
        self.__P2 = 0
        self.__P3 = 0
        self.__F  = 0
        
    def readPhaseVoltage(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x40, 0x02, 0x00, 0x06])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x40, 0x02, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.004)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
        cnt = 0
        data_left = ser.inWaiting()
        while (data_left == 0):
            #wait for data
            cnt=cnt+1
            if (cnt < 50000): #wait for maximum 5 seconds
                sleep(0.0001)
                data_left = ser.inWaiting()
            else:
                print("Transmitting error: Time out")
                return Trans_error;
    
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:15]))
        
        #print (crc_cal) #use for debugging only
    
        crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
        #print (crc_Rx) #use for degugging only
    
        if crc_cal == crc_Rx:
            self.__V1 = struct.unpack('f', received_data[6:2:-1])[0]
            self.__V2 = struct.unpack('f', received_data[10:6:-1])[0]
            self.__V3 = struct.unpack('f', received_data[14:10:-1])[0]
            return No_error;
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error;
            
    def readPhaseCurrent(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x40, 0x12, 0x00, 0x06])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x40, 0x12, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.004)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
        cnt = 0
        data_left = ser.inWaiting()
        while (data_left == 0):
            #wait for data
            cnt=cnt+1
            if (cnt < 50000): #wait for maximum 5 seconds
                sleep(0.0001)
                data_left = ser.inWaiting()
            else:
                print("Transmitting error: Time out")
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:15]))
        crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
        if crc_cal == crc_Rx:
            self.__I1 = struct.unpack('f', received_data[6:2:-1])[0]
            self.__I2 = struct.unpack('f', received_data[10:6:-1])[0]
            self.__I3 = struct.unpack('f', received_data[14:10:-1])[0]      
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
            
    def readPhasePower(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x40, 0x1c, 0x00, 0x06])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x40, 0x1c, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.004)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
        cnt = 0
        data_left = ser.inWaiting()
        while (data_left == 0):
            #wait for data
            cnt=cnt+1
            if (cnt < 50000): #wait for maximum 5 seconds
                sleep(0.0001)
                data_left = ser.inWaiting()
            else:
                print("Transmitting error: Time out")
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:15]))
        crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
        if crc_cal == crc_Rx:
            self.__P1 = struct.unpack('f', received_data[6:2:-1])[0]
            self.__P2 = struct.unpack('f', received_data[10:6:-1])[0]
            self.__P3 = struct.unpack('f', received_data[14:10:-1])[0]       
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error

    def readFrequency(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x40, 0x00, 0x00, 0x02])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x40, 0x00, 0x00, 0x02, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.004)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
        cnt = 0
        data_left = ser.inWaiting()
        while (data_left == 0):
            #wait for data
            cnt=cnt+1
            if (cnt < 50000): #wait for maximum 5 seconds
                sleep(0.0001)
                data_left = ser.inWaiting()
            else:
                print("Transmitting error: Time out")
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:7]))
        crc_Rx = hex(struct.unpack('H',received_data[7:])[0])
    
        if crc_cal == crc_Rx:
            self.__F = struct.unpack('f', received_data[6:2:-1])[0]    
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
#---------------------------------END OF MIC2------------------------------------
#--------------------------------------------------------------------------------
  
class MIC1:
    def __init__(self, Id, Control):
        self.__Control = Control
        self.__Address = Id
        self.__V1 = 0
        self.__V2 = 0
        self.__V3 = 0
        self.__I1 = 0
        self.__I2 = 0
        self.__I3 = 0
        self.__P1 = 0
        self.__P2 = 0
        self.__P3 = 0
        
    def readPhaseVoltage(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x31, 0x00, 0x03])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x31, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
        cnt = 0
        data_left = ser.inWaiting()
        while (data_left == 0):
            #wait for data
            cnt=cnt+1
            if (cnt < 50000): #wait for maximum 5 seconds
                sleep(0.0001)
                data_left = ser.inWaiting()
            else:
                print("Transmitting error: Time out")
                return Trans_error;
    
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:9]))
        
        retval = ""
        for character in received_data:
            retval += ('0123456789ABCDEF'[int(ord(character)/16)])
            retval += ('0123456789ABCDEF'[int(ord(character)%16)])
            retval += ':'
        print (retval[:-1])
        print (crc_cal) #use for debugging only
    
        crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
        #print (crc_Rx) #use for degugging only
    
        if crc_cal == crc_Rx:
            self.__V1 = struct.unpack('H', received_data[4:2:-1])[0]
            self.__V2 = struct.unpack('H', received_data[6:4:-1])[0]
            self.__V3 = struct.unpack('H', received_data[8:6:-1])[0]
            return No_error;
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error;
            
    def readPhaseCurrent(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x39, 0x00, 0x03])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x39, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
        cnt = 0
        data_left = ser.inWaiting()
        while (data_left == 0):
            #wait for data
            cnt=cnt+1
            if (cnt < 50000): #wait for maximum 5 seconds
                sleep(0.0001)
                data_left = ser.inWaiting()
            else:
                print("Transmitting error: Time out")
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:9]))
        crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
        if crc_cal == crc_Rx:
            self.__I1 = struct.unpack('H', received_data[4:2:-1])[0]
            self.__I2 = struct.unpack('H', received_data[6:4:-1])[0]
            self.__I3 = struct.unpack('H', received_data[8:6:-1])[0]      
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
            
    def readPhasePower(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x3E, 0x00, 0x03])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x3E, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
        cnt = 0
        data_left = ser.inWaiting()
        while (data_left == 0):
            #wait for data
            cnt=cnt+1
            if (cnt < 50000): #wait for maximum 5 seconds
                sleep(0.0001)
                data_left = ser.inWaiting()
            else:
                print("Transmitting error: Time out")
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:9]))
        crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
        if crc_cal == crc_Rx:
            self.__P1 = struct.unpack('h', received_data[4:2:-1])[0]
            self.__P2 = struct.unpack('h', received_data[6:4:-1])[0]
            self.__P3 = struct.unpack('h', received_data[8:6:-1])[0]       
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
            
    def readFrequency(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x30, 0x00, 0x01])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x30, 0x00, 0x01, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
        cnt = 0
        data_left = ser.inWaiting()
        while (data_left == 0):
            #wait for data
            cnt=cnt+1
            if (cnt < 50000): #wait for maximum 5 seconds
                sleep(0.0001)
                data_left = ser.inWaiting()
            else:
                print("Transmitting error: Time out")
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:5]))
        crc_Rx = hex(struct.unpack('H',received_data[5:])[0])
    
        if crc_cal == crc_Rx:
            self.__F = struct.unpack('f', received_data[4:2:-1])[0]    
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
#---------------------------------END OF MIC1------------------------------------
#--------------------------------------------------------------------------------