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

#file imports
import uart

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

    uart.convertLength(1)


    ###uart.uartInit()###

    #print(uart.receiveByte())

    #print(uart.receiveByte())

    #print(uart.ser.read())
    #uart.ser.open()
    #dat = uart.receiveBytes(2)
    ###dat = uart.ser.read(11)###

    #datLen = uart.ser.inWaiting()

    #if datLen:
        #dat = dat + uart.ser.read(datLen)
        #print(dat)

    ###print(dat, ":end:") #.decode('ascii')###
    """msg = input("Enter something to send to microcontroller: ")
    uart.ser.write(input(msg.encode()))
    newdat = uart.ser.read(50);
    print(newdat)"""
    
    """
    x = True
    while (x == True):
        msg = input("Enter something to send to microcontroller: ")
        msgLength = len(msg)
        #print("length of message: ", msgLength, "\n")
        uart.ser.write(b'test')
        print("1")
        newdat = uart.ser.read(msgLength) #.decode('ascii')
        print("2")
        print(newdat)
        print("end")"""

if __name__ == "__main__":
    main()