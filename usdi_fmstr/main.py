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
from cmd import convertLength

#file imports
import uart
import cmd
import gui

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
    uart.uartInit()
    count = 0

    #print(uart.receiveBytes(1))
    #print(convertLength(5))

    #cmd.changeVariable(154, "2")

    #send change variable command
    def sendCommandTest():
        val = input("Enter 'y' \n")
        if(val == 'y'):
            #cmd.changeVariable(154, 12)
            valueStr = cmd.getVariable(3)
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
        valueStr = cmd.getVariable(3)
        #sendCommandTest()
        #cmd.changeVariable(34, 4)
        """
        if(valueStr == None):
            valueStr = cmd.getVariable(3)
        """
        print("The value is:", valueStr)
        sleep(.5)

if __name__ == "__main__":
    #main()
    app = gui.UsdiFmstrApp()
    app.run()