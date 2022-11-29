"""
*******************************************************************************
      File Name  : uart.py
      Author     : jdyakimow
      Date       : 11/18/2022
      Description: uart code for usdi freemaster pc application
 ******************************************************************************
"""

#uart msg for changing variable on embedded side [cmd(4 byte)]**[varIDlength(1 byte)]**[var id(variying length)]**[length(1 byte)]**[data[multiple bytes]]


"""
 ******************************************************************************
 * IMPORTS
 ******************************************************************************
"""

#library imports
from lib2to3.pytree import convert
import serial
import string

#file imports

"""
 ******************************************************************************
 * VARIABLES and CONSTANTS
 ******************************************************************************
"""

#communication commands
COMMUNICATION_CHECK = "0x55"
COMMUNICATION_ACK = "0x56"
CHANGE_VARIABLE = "0x51"
READ_VARIABLE = "0x52"
DATA_ACK = "0x53"



#variable type commands
VAR_INT = "0x11"
VAR_CHAR = "0x12"
VAR_STRING = "0x13"
VAR_BOOL = "0x14"


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

"""
 * Function: 		changeVariable(value, numOfBytes, varNumber)
 * Description: 	change variable on embedded side
 * Parameters:		value = the value to change
 *                  numOfBytes = length of value (this might not be needed)
 *                  varNumber = which var to change in ptr array in embedded side
 * Return Value:	None
"""
#TODO: fix types and write embedded code
def changeVariable(value, numOfBytes, varNumber):
    stringBuffer = ""

    #send change variable command (always 4 bytes)
    sendBytes(CHANGE_VARIABLE.encode())

    #send length of variable id int (single char, single byte)
    varIdLen = len(varNumber)
    varIdLength = convertLength(varIdLen)
    sendBytes(varIdLength.encode())

    #send which variable (numeric value for pointer array in embedded system)
    #stringBuffer = str(varNumber)
    sendBytes(varNumber)

    #send length of new value (single char, single byte)
    sendBytes(convertLength(numOfBytes).encode())

    #send data
    sendBytes(value.encode())

    #wait for ack (optional)
    incoming = receiveBytes(1)
    if (incoming == DATA_ACK):
        print("Variable changed")

    #refresh? 

"""
 * Function: 		convertLength(length)
 * Description: 	convert integet to char (1-26) (up to 26 bytes)
 * Parameters:		length = integer to be converted to a char value
 * Return Value:    char length
"""
def convertLength(length):
    d = dict(enumerate(string.ascii_lowercase, 1))
    #print(d[length])
    return d[length]