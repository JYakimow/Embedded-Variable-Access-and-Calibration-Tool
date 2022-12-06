"""
*******************************************************************************
      File Name  : 
      Author     : cmd.py
      Date       : 
      Description: command change functionality
 ******************************************************************************
"""

"""
 ******************************************************************************
 * IMPORTS
 ******************************************************************************
"""

#library imports
from ast import Constant
from reprlib import recursive_repr
import string
import time
#from datetime import datetime

#file imports
import uart

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

#temporary hardcoded value:
CAL_ARRAY_LENGTH = int(34)

"""
 ******************************************************************************
 * FUNCTIONS
 ******************************************************************************
"""

"""
 * Function: 		changeVariable(value, numOfBytes, varNumber)
 * Description: 	send commands and data to change variable on embedded side
 * Parameters:		int value = the new value to send to microcontroller
 *                  int varNumber = which var to change in ptr array in embedded side
 * Return Value:	None
"""
#TODO: fix types and write embedded code
def changeVariable(value, varNumber):
    varNumberStr = ""

    #send change variable command (always 4 bytes)
    uart.sendBytes(CHANGE_VARIABLE.encode())

    #send length of variable id int (single char, single byte)
    varNumberStr = str(varNumber)
    varIdLen = len(varNumberStr)
    varIdLength = convertLength(varIdLen)
    uart.sendBytes(varIdLength.encode())

    #send which variable (numeric value for pointer array in embedded system)
    uart.sendBytes(varNumberStr.encode())

    #check to make sure right varid was sent
    varcheck = uart.receiveBytes(varIdLen)
    print("var ID check: ", varcheck)
    varcheck = varcheck.decode("ascii")
    if(varcheck != varNumberStr):
        #recurive till correct
        changeVariable(value, varNumber)
        return

    #send length of new value (single char, single byte)
    valueStr = str(value) #convert to string
    valueLen = len(valueStr) #get length of value string to transmit
    valueLenChar = convertLength(valueLen)
    uart.sendBytes(valueLenChar.encode()) #send length in char form up to 26 bytes length

    #send data to variable
    uart.sendBytes(valueStr.encode())

    #check to make sure communication happend and call again if didn't
    check = uart.receiveBytes(valueLen)
    print("value check: ", check)
    check = check.decode("ascii")
    if(check == valueStr):
        return
        #print("true")
    else:
        #print("recursion")
        changeVariable(value, varNumber)

def getVariable(varNumber):
    varNumberStr = ""

    #send get variable command (always 4 bytes)
    uart.sendBytes(READ_VARIABLE.encode())

    #send length of variable id int (single char, single byte)
    varNumberStr = str(varNumber)
    varIdLen = len(varNumberStr)
    varIdLength = convertLength(varIdLen)
    uart.sendBytes(varIdLength.encode())

    #send which variable (numeric value for pointer array in embedded system)
    uart.sendBytes(varNumberStr.encode())

    #check to make sure right varid was sent
    varcheck = uart.receiveBytes(varIdLen)
    print("var ID check: ", varcheck)
    varcheck = varcheck.decode("ascii")
    if(varcheck != varNumberStr):
        #recurive till correct
        getVariable(varNumber)
        return

    #get length of new value
    valueLengthString = uart.receiveBytes(1).decode("ascii"); #char right now
    valueLengthInteger = convertLengthBack(valueLengthString) #now an int
    #print("length of value int:", valueLengthInteger)

    #receive value
    valueByteObject = uart.receiveBytes(valueLengthInteger)
    valueString = valueByteObject.decode("ascii")

    #accuracy check
    check1 = valueByteObject
    print("value check1: ", check1)
    check2 = uart.receiveBytes(valueLengthInteger)
    print("value check2: ", check2)

    """
    check1 = str(valueString)
    check2byte = uart.receiveBytes(valueLengthInteger)
    check2bstring = check2byte.decode("ascii")
    check2 = str(check2bstring)
    """

    if(check1 == check2):
        """if(check1 == None or check2 == None or valueString == None):
            getVariable(varNumber)"""
        return check1
    elif(check1 == b'' or check2 == b''):
        getVariable(varNumber)
    elif(check1 == b'' and check2 == b''):
        getVariable(varNumber)
    else:
        #recursion
        getVariable(varNumber)

"""
 * Function: 		convertLength(length)
 * Description: 	convert integet to char (1-26) (up to 26 bytes)
 * Parameters:		length = integer to be converted to a char value
 * Return Value:    char length
"""
def convertLength(length):
    d = dict(enumerate(string.ascii_lowercase, 1))
    return d[length]

"""
 * Function: 		convertLengthBack(aChar)
 * Description: 	convert char to int (1-26) (up to 26 bytes)
 * Parameters:		aChar = char to be converted to int value
 * Return Value:    int value
"""
def convertLengthBack(aChar): #parameter is char
    alphabet = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    count = 0
    
    for i in alphabet:
        count = count + 1
        if alphabet[count] == aChar:
            return count

def getTimeStamp():
    pass