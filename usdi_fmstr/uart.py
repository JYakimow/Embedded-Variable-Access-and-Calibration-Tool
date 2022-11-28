"""
*******************************************************************************
      File Name  : uart.py
      Author     : jyakimow
      Date       : 11/18/2022
      Description: uart code for usdi freemaster pc application
 ******************************************************************************
"""

#uart msg [cmd(4 byte)][length(1 byte)]


"""
 ******************************************************************************
 * IMPORTS
 ******************************************************************************
"""

#library imports
#from ast import Constant
import serial

#file imports

"""
 ******************************************************************************
 * VARIABLES and CONSTANTS
 ******************************************************************************
"""

#communication commands
COMMUNICATION_CHECK = 0x55
COMMUNICATION_ACK = 0x56
CHANGE_VARIABLE = 0x51
READ_VARIABLE = 0x52


#variable type commands
VAR_INT = 0x11
VAR_CHAR = 0x12
VAR_STRING = 0x13
VAR_BOOL = 0x14


#define serial port
ser = serial.Serial() #this must set to com port being used
#ser.close()

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

    #see port info
    print("COM port opened with following settings: ")
    print(ser, '\n')

"""
 * Function: 		sendByte()
 * Description: 	send byte of data
 * Parameters:		None
 * Return Value:	None
"""
def sendBytes(length):
    print("not working yet")

"""
 * Function: 		receiveByte()
 * Description: 	send byte of data
 * Parameters:		None
 * Return Value:	None
"""
def receiveBytes(length):
    data = ser.read(length).decode('ascii')
    return data