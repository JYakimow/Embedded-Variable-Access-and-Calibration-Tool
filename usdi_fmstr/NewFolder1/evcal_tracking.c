/*
 ******************************************************************************
      File Name  : usdi_fmstr_tracking.c
      Author     : jdyak
      Date       : 12/1/2022
      Description: variable tracking for usdi fmstr. (customizable per project) (EVCAT - Embedded Variable Access and Calibration Tool)
 ******************************************************************************
 */

//this file will need to be customized per project in order to access variables that need to be tracked

/*
 ******************************************************************************
 * INCLUDES
 ******************************************************************************
 */

#include <evcal_tracking.h>

/*
 ******************************************************************************
 * DEFINES and CONSTANTS
 ******************************************************************************
 */


//there needs to be a pointer array with all the variables which are
const cal_val_t CAL_LOOKUP_TABLE[] =
{
	{
		.type = TYPE_UINT8,
		.ptr.uint8Ptr = &cals.SPEEDS[SPEED_SLOW].ACCEL_RATE
	},
	{
		.type = TYPE_UINT8,
		.ptr.uint8Ptr = &cals.SPEEDS[SPEED_SLOW].DECEL_RATE
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].START_RPM
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].SPEED_PWM_MULT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].SPEED_ERR_PROP
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].SPEED_ERR_INT
	},
	{
		.type = TYPE_DUTY_CYCLE,
		.ptr.dutycyclePtr = &cals.SPEEDS[SPEED_SLOW].SPEED_DC_INT_LIMIT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].POS_ERR_PROP
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].ON_TIME_ERR_PROP
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].POS_ERR_INT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].ON_TIME_ERR_INT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].DESIRED_RPM
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].MOTOR_STOP_RPM
	},
	{
		.type = TYPE_CURRENT,
		.ptr.currentPtr = &cals.SPEEDS[SPEED_SLOW].MOTOR_CURRENT_LIMIT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].CURRENT_ERR_PROP
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_SLOW].CURRENT_ERR_INT
	},
	{
		.type = TYPE_UINT8,
		.ptr.uint8Ptr = &cals.SPEEDS[SPEED_SLOW].MOTOR_TORQUE_REDUCTION_PERCENT
	},

	//--------------------------------------------
	//NOTE: SPEED_SLOW above && SPEED_FAST below
	//--------------------------------------------

	{
		.type = TYPE_UINT8,
		.ptr.uint8Ptr = &cals.SPEEDS[SPEED_FAST].ACCEL_RATE
	},
	{
		.type = TYPE_UINT8,
		.ptr.uint8Ptr = &cals.SPEEDS[SPEED_FAST].DECEL_RATE
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].START_RPM
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].SPEED_PWM_MULT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].SPEED_ERR_PROP
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].SPEED_ERR_INT
	},
	{
		.type = TYPE_DUTY_CYCLE,
		.ptr.dutycyclePtr = &cals.SPEEDS[SPEED_FAST].SPEED_DC_INT_LIMIT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].POS_ERR_PROP
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].ON_TIME_ERR_PROP
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].POS_ERR_INT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].ON_TIME_ERR_INT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].DESIRED_RPM
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].MOTOR_STOP_RPM
	},
	{
		.type = TYPE_CURRENT,
		.ptr.currentPtr = &cals.SPEEDS[SPEED_FAST].MOTOR_CURRENT_LIMIT
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].CURRENT_ERR_PROP
	},
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.SPEEDS[SPEED_FAST].CURRENT_ERR_INT
	},
	{
		.type = TYPE_UINT8,
		.ptr.uint8Ptr = &cals.SPEEDS[SPEED_FAST].MOTOR_TORQUE_REDUCTION_PERCENT
	},

	// rest of cals below
	{
		.type = TYPE_UINT16,
		.ptr.uint16Ptr = &cals.MOTOR_PWM_FREQ
	}
	/*
	{
		.type = TYPE_UINT8,
		.ptr.uint8Ptr = &cals.MOTORS[0].SECTOR_OFFSET_COR
	},
	{
		.type = TYPE_UINT8,
		.ptr.uint8Ptr = &cals.MOTORS[0].SECTOR_DIR_COR
	},
	{
		.type = TYPE_UINT8,
		.ptr.uint8Ptr = &cals.MOTORS[0].SECTOR_POSITION_REVERSE
	},
	{
		.type = TYPE_UINT8
		.ptr.uint8Ptr = &cals.MOTORS[1].SECTOR_OFFSET_COR
	},
	{
		.type = TYPE_UINT8
		.ptr.uint8Ptr = &cals.MOTORS[1].SECTOR_DIR_COR
	},
	{
		.type = TYPE_UINT8
		.ptr.uint8Ptr = &cals.MOTORS[1].SECTOR_POSITION_REVERSE
	}*/
};

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
 * Function: 		void tracking_varSet(int id, int * ptr);
 * Description: 	set variable value
 * Parameters:		int id = id of variable of location in ptr array
 * 					int * ptr = new value to write
 * Return Value:	none
 */
void tracking_varSet(uint8_t id, int32_t * ptr)
{
    id = id - 1; //id won't be 0 on pc side, so 1 will equal 0. minus to fix that
	switch(CAL_LOOKUP_TABLE[id].type)
	{
		case TYPE_UINT8:
					 *CAL_LOOKUP_TABLE[id].ptr.uint8Ptr = (int)*ptr;
		break;
		case TYPE_UINT16:
					 *CAL_LOOKUP_TABLE[id].ptr.uint16Ptr = (int)*ptr;
		break;
		case TYPE_DUTY_CYCLE:
					 *CAL_LOOKUP_TABLE[id].ptr.dutycyclePtr = (int)*ptr;
		break;
		case TYPE_CURRENT:
					 *CAL_LOOKUP_TABLE[id].ptr.currentPtr = (int)*ptr;
		break;
		case TYPE_TIME:
					 //*CAL_LOOKUP_TABLE[id].ptr.timePtr = (uint32_t)*ptr;
		break;
	}
}

/*
 * Function: 		int tracking_varGet(int id);
 * Description: 	set variable value
 * Parameters:		int id = id of variable of location in ptr array
 * Return Value:	int = value of variable in tracked array
 */
int tracking_varGet(uint8_t id)
{
    id = id - 1; //id won't be 0 on pc side, so 1 will equal 0. minus to fix that
    int anInt = 0;
    int* ptr = &anInt;

	switch(CAL_LOOKUP_TABLE[id].type)
	{
		case TYPE_UINT8:
					 *ptr = *CAL_LOOKUP_TABLE[id].ptr.uint8Ptr;
					 return anInt;
		break;
		case TYPE_UINT16:
					 *ptr = *CAL_LOOKUP_TABLE[id].ptr.uint16Ptr;
					 return anInt;
		break;
		case TYPE_DUTY_CYCLE:
					 *ptr = *CAL_LOOKUP_TABLE[id].ptr.dutycyclePtr;
					 return anInt;
		break;
		case TYPE_CURRENT:
					 *ptr = *CAL_LOOKUP_TABLE[id].ptr.currentPtr;
					 return anInt;
		break;
		case TYPE_TIME:
					 //*ptr = *CAL_LOOKUP_TABLE[id].ptr.timePtr;
					 //return anInt;
		break;
	}
}


/*
 ******************************************************************************
 * Local FUNCTIONS
 ******************************************************************************
 */
