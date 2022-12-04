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
import serial

#file imports

"""
 ******************************************************************************
 * VARIABLES and CONSTANTS
 ******************************************************************************
"""

#define serial port
ser = serial.Serial() #this must set to com port being used
#ser.close()
#uart.ser.inWaiting()

"""
 ******************************************************************************
 * FUNCTIONS
 ******************************************************************************
"""

"""
 * Function: 		uartInit()
 * Description: 	initialize uart serial port settings
 * Parameters:		None
 * Return Value:	None
"""
def uartInit():
    ser.baudrate = 115200   #set baudrate
    ser.port = 'COM3'       #set com port
    #ser.timeout = 1        #timeout after one read
    ser.open()              #open connection
    ser.timeout = 1

    #see port info
    print("COM port opened with following settings: ")
    print(ser, '\n')

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