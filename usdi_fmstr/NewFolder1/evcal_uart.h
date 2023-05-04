/*
 ******************************************************************************
      File Name  : uart_drivers.h
      Author     : jdyakimow
      Date       : 11/08/2022
      Description: uart communication drivers for usdi fmstr
 ******************************************************************************
 */

//baud rate is 115200 (9600 is common also)

#ifndef UART_DRIVERS_H
#define UART_DRIVERS_H

/*
 ******************************************************************************
 * INCLUDES
 ******************************************************************************
 */

#include "gpio.h"
#include "stdio.h"
#include "DiagPort.h"
#include "derivative.h"
#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

/*
 ******************************************************************************
 * DEFINES, CONSTANTS, ENUMS, STRUCTS
 ******************************************************************************
 */

/*
 ******************************************************************************
 * GLOBAL VARIABLES
 ******************************************************************************
 */

/*
 ******************************************************************************
 * GLOBAL FUNCTION PROTOTYPES
 ******************************************************************************
 */

/*
 * Function: 		void Uart_Init(void);
 * Description: 	initialize everything needed for UART communication.
 * Parameters:		None
 * Return Value:	None
 */
void Uart_Init(void);

/*
 * Function: 		void uart_testSendReceive(void);
 * Description: 	test communication receiving and sending
 * Parameters:		None
 * Return Value:	None
 */
void uart_testSendReceive(void);

/*
 * Function: 		void uart_interpret_cmd(void);
 * Description: 	command byte handler
 * Parameters:		int cmd_value[]
 * Return Value:	None
 */
//void uart_interpret_cmd(void);

/*
 * Function: 		void uart_transmit(void * dataPtr, uint8_t length)
 * Description: 	transmit function for cross compatibility with other boards. can be easily rewritten to work with other uart drivers
 * Parameters:		dataPtr = data to transmit
 * 					length = length in bytes of data to transmit
 * Return Value:	None
 */
void uart_transmit(void * dataPtr, uint8_t length);

/*
 * Function: 		void uart_recieve(void * dataPtr, uint8_t length);
 * Description: 	receive function for cross compatibility with other boards. can be easily rewritten to work with other UART drivers
 * Parameters:		dataPtr = data to transmit
 * 					length = length in bytes of data to receive
 * Return Value:	None
 */
void uart_receive(void * dataPtr, uint8_t length);

/*
 * Function: 		int uart_getReceiveCount(void);
 * Description: 	function to get number of bytes in uart recieving buffer
 * Parameters:		None
 * Return Value:	int number of bytes in uart fifo buffer
 */
int uart_getReceiveCount(void);

#endif
