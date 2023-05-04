/*
 ******************************************************************************
      File Name  : evcal.h
      Author     : jdyakimow
      Date       : 11/15/2022
      Description: evcal functionality
 ******************************************************************************
 */

#ifndef USDI_FMSTR_H
#define USDI_FMSTR_H

/*
 ******************************************************************************
 * INCLUDES
 ******************************************************************************
 */

#include <evcal_tracking.h>
#include <evcal_uart.h>
#include <stdint.h>
#include <stdio.h>

/*
 ******************************************************************************
 * DEFINES, CONSTANTS, ENUMS, STRUCTS
 ******************************************************************************
 */

typedef enum
{
	WAITING_FOR_COMMAND,
	COMMAND_RECIEVED,
	HANDLE_COMMAND
	//FINISH_COMMAND
} poll_state_t;

typedef enum
{
	COMM_CHECK_UNUSED,
	COMM_CHECK_START,
	COMM_CHECK_DELAY
} comm_check_t;

typedef enum
{
	CHANGE_VAR_IDLE,
	CHANGE_VAR_START,
	CHANGE_VAR_DELAY
} change_var_t;

typedef enum
{
	SEND_VAR_UNUSED,
	SEND_VAR_START,
	SEND_VAR_DELAY
} send_var_t;

typedef enum
{
	NO_COMMAND,
	CHANGE_VARIABLE_CMD,
	READ_VARIABLE_CMD,
	COMM_CHECK_CMD
} current_cmd_state_t;

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

void evcal_init(void);

/*
 * Function: 		void evcalPoll(void);
 * Description: 	poll once per loop to listen for uart
 * Parameters:		None
 * Return Value:	None
 */
void evcalPoll(void);

/*
 * Function: 		void evcal_interpretCmd(void);
 * Description: 	handle command received over uart and call functions linked to that command
 * Parameters:		None
 * Return Value:	None
 */
void evcal_interpretCmd(void);

/*
 * Function: 		void evcal_communicationCheck(void);
 * Description: 	send 0x56 back to pc after receiving command to check if communication is working
 * Parameters:		None
 * Return Value:	None
 */
void evcal_communicationCheck(void);

/*
 * Function: 		void evcal_changeVariable(void);
 * Description: 	receive new value of variable over uart then write to variable the new value
 * Parameters:		None
 * Return Value:	None
 */
void evcal_changeVariable(void);

/*
 * Function: 		void evcal_sendVariable(void);
 * Description: 	get value of variable and send to pc over uart
 * Parameters:		None
 * Return Value:	None
 */
void evcal_sendVariable(void);

#endif
