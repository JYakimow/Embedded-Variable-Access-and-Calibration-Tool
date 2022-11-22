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

#file imports
from pickle import TRUE
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

    uart.uartInit()

    #print(uart.receiveByte())

    #print(uart.receiveByte())

    #print(uart.ser.read())
    #uart.ser.open()
    dat = uart.receiveBytes(12)
    print(dat)
    """msg = input("Enter something to send to microcontroller: ")
    uart.ser.write(input(msg.encode()))
    newdat = uart.ser.read(50);
    print(newdat)"""
    
    x = True
    while (x == True):
        msg = input("Enter something to send to microcontroller: ")
        msgLength = len(msg)
        #print("length of message: ", msgLength, "\n")
        uart.ser.write(b'test')
        print("1")
        newdat = uart.ser.read(4) #.decode('ascii')
        print("2")
        print(newdat)
        print("end")

if __name__ == "__main__":
    main()