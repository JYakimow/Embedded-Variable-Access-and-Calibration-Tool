/*
 ******************************************************************************
      File Name  : usdi_fmstr_tracking.h
      Author     : jdyak
      Date       : 12/1/2022
      Description: variable tracking for usdi fmstr. (customizable per project) (EVCAT - Embedded Variable Access and Calibration Tool)
 ******************************************************************************
 */

//NOTE: put variables that you want tracked in this file in an array. Array position is the id for communication and identification on PC end of things

#ifndef EVCAL_TRACKING_H_
#define EVCAL_TRACKING_H_

/*
 ******************************************************************************
 * INCLUDES
 ******************************************************************************
 */

#include <stdint.h>
#include "Cals.h"

/*
 ******************************************************************************
 * DEFINES, CONSTANTS, ENUMS, STRUCTS
 ******************************************************************************
 */

//set length of variable pointer array here
#define POINTER_ARRAY_LENGTH 35

typedef enum
{
	TYPE_UINT8 = 0,
	TYPE_UINT16,
	TYPE_DUTY_CYCLE,
	TYPE_CURRENT,
	TYPE_TIME
} cal_types_t;

typedef union
{
   volatile uint8_t * uint8Ptr;
   volatile uint16_t * uint16Ptr;
   volatile duty_cycle_t * dutycyclePtr;
   volatile current_t * currentPtr;
   volatile sw_timer_t timePtr;
} cal_ptr_union_t;

typedef struct
{
   cal_types_t type;
   cal_ptr_union_t ptr;
} cal_val_t;

const cal_val_t CAL_LOOKUP_TABLE[POINTER_ARRAY_LENGTH];

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
 * Function: 		void tracking_varSet(int id, int * ptr);
 * Description: 	set variable value
 * Parameters:		int id = id of variable of location in ptr array
 * 					int * ptr = new value to write
 * Return Value:	none
 */
void tracking_varSet(uint8_t id, int32_t * ptr);

/*
 * Function: 		int tracking_varGet(int id);
 * Description: 	set variable value
 * Parameters:		int id = id of variable of location in ptr array
 * Return Value:	int = value of variable in tracked array
 */
int tracking_varGet(uint8_t id);

#endif /* USDI_FMSTRTRACKING_H_ */
