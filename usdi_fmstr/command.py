"""
*******************************************************************************
      File Name  : command.py
      Author     : jdyak
      Date       : 11/18/2022
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
import datetime
import configparser

#file imports
import uart
import application
import debug_logging as log

"""
 ******************************************************************************
 * VARIABLES and CONSTANTS
 ******************************************************************************
"""

#communication commands
COMMUNICATION_CHECK = "5" #formerly "0x55"
COMMUNICATION_ACK = "6" #formerly "0x56"
CHANGE_VARIABLE = "1" #formerly "0x51"
READ_VARIABLE = "2" #formerly 0x52
DATA_ACK = "0x53"

#variable type commands (not currently used)
VAR_INT = "0x11"
VAR_CHAR = "0x12"
VAR_STRING = "0x13"
VAR_BOOL = "0x14"

#temporary hardcoded value:
#CAL_ARRAY_LENGTH = 35

"""
 ******************************************************************************
 * FUNCTIONS
 ******************************************************************************
"""

"""
#def init():
#    config = configparser.ConfigParser()
#    config.read('config\config.ini')
#    CAL_ARRAY_LENGTH = config['CONFIG']['VAR_ARRAY_LENGTH']
    #print(CAL_ARRAY_LENGTH)"""
    

"""
 * Function: 		testConnection()
 * Description: 	send test command and recieve check
 * Parameters:		none
 * Return Value:	true or false
"""
def testConnection():
    #send check connection command
    
    cmd_msg = COMMUNICATION_CHECK
    for i in range(19):
        cmd_msg = cmd_msg + " "
        #print(i)
    #print(cmd_msg, ";")

    uart.sendBytes(cmd_msg.encode())

    check = uart.receiveBytes(1).decode("ascii")
    if(check == COMMUNICATION_ACK):
        return True
    else:
        return False

"""
 * Function: 		changeVariable(value, numOfBytes, varNumber)
 * Description: 	send commands and data to change variable on embedded side
 * Parameters:		int value = the new value to send to microcontroller
 *                  int varNumber = which var to change in ptr array in embedded side
 * Return Value:	None
"""
def changeVariable(value, varNumber):
    try:
        uartMsgString = ""

        #set position 0 to command
        uartMsgString = str(uartMsgString) + str(READ_VARIABLE)

        #set position 1 to length of varNumber
        varIDlen = determineLength(varNumber)
        uartMsgString = str(uartMsgString) + str(varIDlen)

        #set position 2 - 4 to varID
        if(varIDlen == 1):
            uartMsgString = str(uartMsgString) + str(varNumber) #takes up one space
            uartMsgString = str(uartMsgString) + "  " #add two spaces
        elif(varIDlen == 2):
            uartMsgString = str(uartMsgString) + str(varNumber) #takes up two spaces
            uartMsgString = str(uartMsgString) + " " #add one spaces
        elif(varIDlen == 3):
            uartMsgString = str(uartMsgString) + str(varNumber) #takes up three spaces

        #set position 5 to value length
        valueLen = determineLength(value)
        uartMsgString = str(uartMsgString) + str(valueLen)

        #set positions 6 - 20 to value or blank
        if(valueLen == 1):
            uartMsgString = str(uartMsgString) + str(value) #takes up 1 space
            uartMsgString = str(uartMsgString) + "              " #add 14 spaces
        elif(valueLen == 2):
            uartMsgString = str(uartMsgString) + str(value) #takes up 2 spaces
            uartMsgString = str(uartMsgString) + "             " #add 13 spaces
        elif(valueLen == 3):
            uartMsgString = str(uartMsgString) + str(value) #takes up 3 spaces
            uartMsgString = str(uartMsgString) + "            " #add 12 spaces
        elif(valueLen == 4):
            uartMsgString = str(uartMsgString) + str(value) #takes up 4 spaces
            uartMsgString = str(uartMsgString) + "           " #add 11 spaces
        elif(valueLen == 5):
            uartMsgString = str(uartMsgString) + str(value) #takes up 5 spaces
            uartMsgString = str(uartMsgString) + "          " #add 10 spaces
        elif(valueLen == 6):
            uartMsgString = str(uartMsgString) + str(value) #takes up 6 spaces
            uartMsgString = str(uartMsgString) + "         " #add 9 spaces
        elif(valueLen == 7):
            uartMsgString = str(uartMsgString) + str(value) #takes up 7 spaces
            uartMsgString = str(uartMsgString) + "        " #add 8 spaces
        elif(valueLen == 8):
            uartMsgString = str(uartMsgString) + str(value) #takes up 8 spaces
            uartMsgString = str(uartMsgString) + "       " #add 7 spaces
        elif(valueLen == 9):
            uartMsgString = str(uartMsgString) + str(value) #takes up 9 spaces
            uartMsgString = str(uartMsgString) + "      " #add 6 spaces
        elif(valueLen == 10):
            uartMsgString = str(uartMsgString) + str(value) #takes up 10 spaces
            uartMsgString = str(uartMsgString) + "     " #add 5 
        elif(valueLen == 11):
            uartMsgString = str(uartMsgString) + str(value) #takes up 11 spaces
            uartMsgString = str(uartMsgString) + "    " #add 4 spaces
        elif(valueLen == 12):
            uartMsgString = str(uartMsgString) + str(value) #takes up 12 spaces
            uartMsgString = str(uartMsgString) + "   " #add 3 spaces
        elif(valueLen == 13):
            uartMsgString = str(uartMsgString) + str(value) #takes up 13 spaces
            uartMsgString = str(uartMsgString) + "  " #add 2 
        elif(valueLen == 14):
            uartMsgString = str(uartMsgString) + str(value) #takes up 14 spaces
            uartMsgString = str(uartMsgString) + " " #add 1 spaces
        elif(valueLen == 15):
            uartMsgString = str(uartMsgString) + str(value) #takes up 15 spaces
            uartMsgString = str(uartMsgString) + "" #add 0 spaces

        #set rest of message to blank ascii
        #uartMsgString = str(uartMsgString) + "               "



        """
        #transmit over uart
        uart.sendBytes(uartMsgString.encode())
        print(uartMsgString, ":")

        #listen over uart
        incomingLenChar = uart.receiveBytes(1) #uart.ser.readline() #uart.receiveBytes(11)
        incomingLen = convertLengthBack(incomingLenChar.decode())
        incoming = uart.receiveBytes(incomingLen) #uart.ser.readline() #uart.receiveBytes(incomingLen)
        print(incomingLenChar)
        #print(incomingLen)
        print(incoming) #.decode())
        """

        #return #incoming.decode()
        
    except Exception as ex:
        print(datetime.datetime.now(), "LOG: Error:", ex, "\n")
        """
        x = getVariable(varNumber)
        return x
        """
        #gui.tk.messagebox.showerror(title="Error", message=ex)


"""
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
"""

"""
 * Function: 		getVariable(varNumber)
 * Description: 	get value of variable on embedded system
 * Parameters:		varNumber = integer of which var to change in pointer array in embedded side
 * Return Value:	x = integer of variable on embedded side
"""
def getVariable(varNumber):
    try:
        uartMsgString = ""

        #set position 0 to command
        uartMsgString = str(uartMsgString) + str(READ_VARIABLE)

        #set position 1 to length of varNumber
        varIDlen = determineLength(varNumber)
        uartMsgString = str(uartMsgString) + str(varIDlen)

        #set position 2 - 4 to varID
        if(varIDlen == 1):
            uartMsgString = str(uartMsgString) + str(varNumber) #takes up one space
            uartMsgString = str(uartMsgString) + "  " #add two spaces
        elif(varIDlen == 2):
            uartMsgString = str(uartMsgString) + str(varNumber) #takes up two spaces
            uartMsgString = str(uartMsgString) + " " #add one spaces
        elif(varIDlen == 3):
            uartMsgString = str(uartMsgString) + str(varNumber) #takes up three spaces

        #set rest of message to blank ascii
        uartMsgString = str(uartMsgString) + "               "

        #transmit over uart
        uart.sendBytes(uartMsgString.encode())
        print(uartMsgString, ":")

        #listen over uart
        incomingLenChar = uart.receiveBytes(1) #uart.ser.readline() #uart.receiveBytes(11)
        incomingLen = convertLengthBack(incomingLenChar.decode())
        incoming = uart.receiveBytes(incomingLen) #uart.ser.readline() #uart.receiveBytes(incomingLen)
        print(incomingLenChar)
        #print(incomingLen)
        print(incoming) #.decode())

        return incoming.decode()
        
    except Exception as ex:
        print(datetime.datetime.now(), "LOG: Error:", ex, "\n")
        x = getVariable(varNumber)
        return x
        #gui.tk.messagebox.showerror(title="Error", message=ex)

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
    
    for val in range(27):
        aInt = val + 1
        count = count + 1
        if alphabet[aInt] == aChar:
            return count

#determine length of num
def determineLength(number):
    if(number <= 9):
        return 1
    elif(number >= 10 and number < 100):
        return 2
    elif(number >= 100 and number < 1000):
        return 3
    elif(number >= 1000 and number < 10000):
        return 4
    elif(number >= 10000 and number < 100000):
        return 5
    elif(number >= 100000 and number < 1000000):
        return 6
    elif(number >= 1000000 and number < 10000000):
        return 7
    elif(number >= 10000000 and number < 100000000):
        return 8
    elif(number >= 100000000 and number < 1000000000):
        return 9