"""
*******************************************************************************
      File Name  : uart.py
      Author     : jdyakimow
      Date       : 11/18/2022
      Description: uart code for usdi freemaster pc application
 ******************************************************************************
"""

#uart msg for changing variable on embedded side [cmd(4 byte)]**[varIDlength(1 byte)]**[var id(variying length)]**[length(1 byte)]**[data(multiple bytes)]

"""
 ******************************************************************************
 * IMPORTS
 ******************************************************************************
"""

#library imports
from lib2to3.pytree import convert
from wsgiref.validate import PartialIteratorWrapper
import serial
import serial.tools.list_ports
import datetime

#file imports
import application
import command
import debug_logging as log

"""
 ******************************************************************************
 * VARIABLES and CONSTANTS
 ******************************************************************************
"""

#define serial port
ser = serial.Serial() #this must set to com port being used
ser.close()
#uart.ser.inWaiting()

"""
 ******************************************************************************
 * FUNCTIONS
 ******************************************************************************
"""

"""
 * Function: 		init()
 * Description: 	initialize uart serial port settings
 * Parameters:		None
 * Return Value:	None
"""
def init(port, baud, dataBits, stopBits, parityChecking): #, baud, dataBits, stopBits, parity) 
    ser.port = port 
    ser.baudrate = baud   
    ser.bytesize = handleUartByteSize(dataBits)
    ser.stopbits = convertStopBits(stopBits)
    ser.parity = convertParity(parityChecking)
    ser.timeout = .25 #1 second to read before timeout
    ser.open()

    log_msg = "COM port opened with following settings: \n" + str(ser)
    log.info(log_msg)

"""
 * Function: 		getPorts()
 * Description: 	send byte of data
 * Parameters:		None
 * Return Value:	portList (python list)
"""
def getPorts():
    ports = serial.tools.list_ports.comports()
    portList = []
    for port, desc, hwid in sorted(ports):
        thePort = "{}".format(port)
        portList.append(thePort)
        #ports1 = "{}: {} [{}]".format(port, desc, hwid)
    return portList

"""
 * Function: 		sendByte(data)
 * Description: 	send byte of data
 * Parameters:		data = data to be sent over uart
 * Return Value:	None
"""
def sendBytes(data):
    ser.write(data)

"""
 * Function: 		receiveBytes()
 * Description: 	receive bytes of data
 * Parameters:		None
 * Return Value:	read data from uart
"""
def receiveBytes(length):
    data = ser.read(length) #.decode('ascii')
    return data

def closeConnection():
    ser.close()

def handleUartByteSize(dataByte):
    dataByte = str(dataByte)

    if(dataByte == "5bits"):
        return serial.FIVEBITS
    elif(dataByte == "6bits"):
        return serial.SIXBITS
    elif(dataByte == "7bits"):
        return serial.SEVENBITS
    elif(dataByte == "8bits"):
        return serial.EIGHTBITS

def convertStopBits(stopbit):
    stopbit = str(stopbit)

    if(stopbit == "one"):
        return serial.STOPBITS_ONE
    elif(stopbit == "two"):
        return serial.STOPBITS_TWO

def convertParity(parity):
    parity = str(parity)

    if(parity == "none"):
        return serial.PARITY_NONE
    elif(parity == "even"):
        return serial.PARITY_EVEN
    elif(parity == "odd"):
        return serial.PARITY_ODD