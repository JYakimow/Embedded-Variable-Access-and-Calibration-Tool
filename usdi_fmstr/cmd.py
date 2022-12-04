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
from reprlib import recursive_repr
import string
import time

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

"""
 ******************************************************************************
 * FUNCTIONS
 ******************************************************************************
"""

"""
 * Function: 		changeVariable(value, numOfBytes, varNumber)
 * Description: 	change variable on embedded side
 * Parameters:		int value = the value to change
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


    """
    #send length of new value (single char, single byte)
    uart.sendBytes(convertLength(numOfBytes).encode())

    #send data
    uart.sendBytes(value.encode())"""


    #check to make sure communication happend and call again if didn't (should be at end basically read)
    check = uart.receiveBytes(varIdLen)
    print(check)
    check = check.decode("ascii")
    if(check == varNumberStr):
        return
        #print("true")
    else:
        #print("recursion")
        changeVariable(value, varNumber)


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
