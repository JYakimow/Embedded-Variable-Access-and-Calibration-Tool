/*
*******************************************************************************
      File Name  : uart_drivers.c
      Author     : jdyakimow
      Date       : 11/08/2022
      Description: uart communication drivers for usdi fmstr
 ******************************************************************************
 */

/*
 ******************************************************************************
 * INCLUDES
 ******************************************************************************
 */

#include <evcal_uart.h>

/*
 ******************************************************************************
 * DEFINES and CONSTANTS
 ******************************************************************************
 */

//#define CHANGE_VARIABLE 0x51

/*
 ******************************************************************************
 * GLOBAL VARIABLES
 ******************************************************************************
 */

/*
 ******************************************************************************
 * LOCAL TYPES
 ******************************************************************************
 */

/*
 ******************************************************************************
 * LOCAL VARIABLES (declare as static)
 ******************************************************************************
 */

static char conversionBufferArr[50];
//static char *conversionBufferArrPtr = conversionBufferArr;

/*
 ******************************************************************************
 * LOCAL FUNCTION PROTOTYPES (declare as static)
 ******************************************************************************
 */

/*
 ******************************************************************************
 * GLOBAL FUNCTIONS
 ******************************************************************************
 */

/*
 * Function: 		void Uart_Init(void);
 * Description: 	initialize everything needed for UART communication.
 * Parameters:		None
 * Return Value:	None
 */
void Uart_Init(void)
{
	//device specific uart inits
	DP_Init();
}

/*
 * Function: 		void uart_transmit(void * dataPtr, uint8_t length);
 * Description: 	transmit function for cross compatibility with other boards. can be easily rewritten to work with other uart drivers
 * Parameters:		dataPtr = data to transmit
 * 					length = length in bytes of data to transmit
 * Return Value:	None
 */
void uart_transmit(void * dataPtr, uint8_t length)
{
	//code here
	DP_Transmit(dataPtr, length);
}

/*
 * Function: 		void uart_recieve(void * dataPtr, uint8_t length);
 * Description: 	receive function for cross compatibility with other boards. can be easily rewritten to work with other UART drivers
 * Parameters:		dataPtr = data to transmit
 * 					length = length in bytes of data to receive
 * Return Value:	None
 */
void uart_receive(void * dataPtr, uint8_t length)
{
	DP_Receive(dataPtr, length);
}

/*
 * Function: 		int uart_getReceiveCount(void);
 * Description: 	function to get number of bytes in uart recieving buffer
 * Parameters:		None
 * Return Value:	int number of bytes in uart fifo buffer
 */
int uart_getReceiveCount(void)
{
	int a = DP_GetReceiveCount();
	return a;
}

/*
 ******************************************************************************
 * Local FUNCTIONS (declare as static)
 ******************************************************************************
 */
