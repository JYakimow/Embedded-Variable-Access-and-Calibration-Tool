"""
*******************************************************************************
      File Name  : main.py
      Author     : jdyakimow
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
    print("Application Launched\n")

    #init uart communication
    uart.init('COM3', 115200, '8bits', 'one', 'none')
    #debug.initLogging()
    count = 0

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
    while(True):
        print("****** loop restarted", count, "******")
        count = count + 1
        valueStr = command.getVariable(3)
        #sendCommandTest()
        #command.changeVariable(34, 4)
        """
        if(valueStr == None):
            valueStr = cmd.getVariable(3)
        """
        print("The value is:", valueStr)
        sleep(.1)

if __name__ == "__main__":
    #main()
    command.init()
    app = application.UsdiFmstrApp()
    app.run()
    #log.debug("this is a test")
    #log.error("test")