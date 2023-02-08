"""
*******************************************************************************
      File Name  : main.py
      Author     : jdyak
      Date       : 11/18/2022
      Description: main file for usdi freemaster pc application
 ******************************************************************************
"""

"""
 ******************************************************************************
 * IMPORTS
 ******************************************************************************
"""

#library imports
from pickle import TRUE
from time import sleep
from tkinter.tix import Tree
from command import convertLength
import xml.etree.ElementTree as ET


#file imports
import uart
import application
import command
import debug_logging as log

"""
 ******************************************************************************
 * VARIABLES and CONSTANTS
 ******************************************************************************
"""

"""
 ******************************************************************************
 * FUNCTIONS
 ******************************************************************************
"""

def main():
    #command.init()
    app = application.UsdiFmstrApp()
    app.run()

    #print("Application Launched\n")

    #init uart communication
    #uart.init('COM3', 115200, '8bits', 'one', 'none')
    #debug.initLogging()
    #count = 0

    #print("received:", uart.receiveBytes(5))

    #print(uart.receiveBytes(1))
    #print(convertLength(5))

    #cmd.changeVariable(154, "2")

    #send change variable command
    def sendCommandTest():
        val = input("Enter 'y' \n")
        if(val == 'y'):
            #cmd.changeVariable(154, 12)
            valueStr = command.getVariable(3)
            """
            uart.sendBytes(b'0x51') #0x51
            print(cmd.CHANGE_VARIABLE.encode(), "was sent")
            #print("'page' was sent")
            rec = uart.ser.read(4)
            print(rec) #.decode("ascii"))"""
        """
        val2 = input("Enter 'a' \n")
        if(val2 == 'a'):
            print("Received Value: ", uart.receiveBytes(1))"""

    #enter main loop
    
    """
    while(True):
        print("****** loop restarted", count, "******")
        count = count + 1
        valueStr = command.getVariable(3)
        #sendCommandTest()
        #command.changeVariable(34, 4)
        
        #if(valueStr == None):
        #    valueStr = cmd.getVariable(3)
        
        print("The value is:", valueStr)
        sleep(.1)
        """

def testing():
    uart.init('COM4', 115200, '8bits', 'one', 'none')
    #debug.initLogging()
    count = 0

    print("received:", uart.receiveBytes(5))

    #send bytes
    uart.sendBytes(b'page')
    print("new received:", uart.receiveBytes(4))

def xmlParseTest():
    tree = ET.parse("variable_names.xml")
    root = tree.getroot()
    for i in root.findall('var'):
        idVal = i.find('id').text
        varName = i.find('name').text
        print("ID:", idVal)
        print("Variable Name:", varName)

#simulate "main" function in python
if __name__ == "__main__":
    main()