/*
*******************************************************************************
y
      File Name  : evcal.c
      Author     : jdyakimow
      Date       :
      Description: usdi freemaster functions
 ******************************************************************************
 */

/*
 ******************************************************************************
 * INCLUDES
 ******************************************************************************
 */

#include <evcal.h>

/*
 ******************************************************************************
 * DEFINES and CONSTANTS
 ******************************************************************************
 */

//commands
#define CHANGE_VARIABLE 1			//formerly 0x51
#define READ_VARIABLE 2				//formerly 0x52
#define DATA_ACK 3 					//formerly 0x53
#define COMMUNICATION_CHECK 5 		//formerly 0x55
#define COMMUNICATION_ACK 6 		//formerly 0x56

//uart message lengths
#define ONE_BYTE 1
#define FOUR_BYTES 4
#define TWENTY_BYTES 20
#define ELEVEN_BYTES 11

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

//state machine
poll_state_t poll_state;
current_cmd_state_t selected_command_state;
comm_check_t comm_check_state;
send_var_t send_var_state;
change_var_t change_var_state;

//other variables
char cmd = 0;
char uartMsgArr[TWENTY_BYTES];             // ***empty***
char *uartMsgArrPtr = uartMsgArr;
char bufferArr[FOUR_BYTES]; //length of 4
char *bufferArrPtr = bufferArr;
uint8_t lenBufferChar = 0;
uint8_t valueLenChar = 0;
uint8_t lenID = 0;
uint8_t valueLen = 0;
//char varID[10] = "";
//char *varIDPtr = varID;
uint8_t address = 0;
char valueArr[10];                             // ***empty***
char *valueArrPtr = valueArr;
int32_t value = 0;
int32_t *valuePtr = &value;
int valueInt = 0;
char sendBuffer[11];                          // ***empty***
char *sendBufferPtr = sendBuffer;
char tempConversionBuffer;

/*
 ******************************************************************************
 * LOCAL FUNCTION PROTOTYPES (declare as static)
 ******************************************************************************
 */

//static void intToChar(int anInt, char *resultPtr);

static int charToInt(char *charPtr);

static int charToHex(char *charPtr);

static uint8_t convertBack(uint8_t aChar);

static char convertInt(uint8_t anInt);

int getArrayFilledLength(char array[], uint8_t length);

/*
 ******************************************************************************
 * GLOBAL FUNCTIONS
 ******************************************************************************
 */

void evcal_init(void)
{
	//set states to unused state
	selected_command_state = NO_COMMAND;
	comm_check_state = COMM_CHECK_UNUSED;
	poll_state = WAITING_FOR_COMMAND;
	send_var_state = SEND_VAR_UNUSED;
	change_var_state = CHANGE_VAR_IDLE;
}

/*
 * Function: 		void evcalPoll(void);
 * Description: 	poll once per loop to listen for uart
 * Parameters:		None
 * Return Value:	None
 */
void evcalPoll(void)
{
	switch(poll_state)
	{
		case WAITING_FOR_COMMAND: //waiting for the command to arrive state
		{
			//if 1 bytes in buffer (should only be case when receiving commands)(command will be first thing since pc will be set as a master)
			uint8_t theLengthOfBuffer = 0;
			theLengthOfBuffer = uart_getReceiveCount();
			if(theLengthOfBuffer >= TWENTY_BYTES) //== but currently using >=
			{
				poll_state = COMMAND_RECIEVED;
				evcal_interpretCmd();
			}
			/*
			else if(theLengthOfBuffer > TWENTY_BYTES) //greater than
			{
				uint8_t temp_delete_buffer[50];
				uint8_t *temp_delete_buffer_ptr = temp_delete_buffer;
				uart_receive(temp_delete_buffer_ptr, TWENTY_BYTES);
			}*/
			break;
		}
		case COMMAND_RECIEVED: //state for reading in the command and selecting proper command
		{
			evcal_interpretCmd();
			//in evcal_interpretCmd(); it will recieve and set to handle_Command state
			break;
		}
		case HANDLE_COMMAND:
		{
			switch(selected_command_state)
			{
				case NO_COMMAND:
				{
					selected_command_state = NO_COMMAND;
					comm_check_state = COMM_CHECK_UNUSED;
					poll_state = WAITING_FOR_COMMAND;
					send_var_state = SEND_VAR_UNUSED;
					change_var_state = CHANGE_VAR_IDLE;
					break;
				}
				case CHANGE_VARIABLE_CMD:
				{
					evcal_changeVariable();
					break;
				}
				case READ_VARIABLE_CMD:
				{
					evcal_sendVariable();
					break;
				}
				case COMM_CHECK_CMD:
				{
					//comm_check_state = COMM_CHECK_START;
					evcal_communicationCheck();

					break;
				}
			}
			break;
		}
		default:
		{
			selected_command_state = NO_COMMAND;
			comm_check_state = COMM_CHECK_UNUSED;
			poll_state = WAITING_FOR_COMMAND;
			send_var_state = SEND_VAR_UNUSED;
			change_var_state = CHANGE_VAR_IDLE;
			break;
		}
	}
}

/*
 * Function: 		void evcal_interpretCmd(void);
 * Description: 	handle command received over uart and call functions linked to that command
 * Parameters:		None
 * Return Value:	None
 */
void evcal_interpretCmd(void)
{
	switch(poll_state)
	{
		case WAITING_FOR_COMMAND:
		{
			//code should never reach this point.
			break;
		}
		case COMMAND_RECIEVED:
		{
			uart_receive(uartMsgArrPtr, TWENTY_BYTES); //receive uart message
			//this has to be char or it breaks
			char commandAscii = uartMsgArr[0]; //charToInt(&uartMsgArr[0]);
			uint8_t command = charToInt(&commandAscii);
			poll_state = HANDLE_COMMAND; //set to state to handle command.

			//if command equals change variable then call change variable code
			if(command == CHANGE_VARIABLE)
			{
				selected_command_state = CHANGE_VARIABLE_CMD;
				change_var_state = CHANGE_VAR_START;
				//evcal_changeVariable();
			}
			//if command is read variable call
			else if(command == READ_VARIABLE)
			{
				selected_command_state = READ_VARIABLE_CMD;
				send_var_state = SEND_VAR_START;
				//evcal_sendVariable();
			}
			else if(command == COMMUNICATION_CHECK)
			{
				selected_command_state = COMM_CHECK_CMD;
				comm_check_state = COMM_CHECK_START;
				//evcal_communicationCheck();
			}
			//TODO: add statement for if no valid command in message
			break;
		}
		case HANDLE_COMMAND:
		{
			//call evcal interpret (code shouldn't reach here so ignore.)
			break;
		}
	}
}

/*
 * Function: 		void evcal_communicationCheck(void);
 * Description: 	send 0x56 back to pc after receiving command to check if communication is working
 * Parameters:		None
 * Return Value:	None
 */
void evcal_communicationCheck(void)
{
	switch(comm_check_state)
	{
		case COMM_CHECK_UNUSED:
		{
			//should never reach here
			break;
		}
		case COMM_CHECK_START:
		{
			//break and delay (python uart library is slow)
			comm_check_state = COMM_CHECK_DELAY;
			break;
		}
		case COMM_CHECK_DELAY:
		{
			//send communication ack and reset states to unused
			uart_transmit("6", ONE_BYTE);

			//set states to unused state
			selected_command_state = NO_COMMAND;
			comm_check_state = COMM_CHECK_UNUSED;
			poll_state = WAITING_FOR_COMMAND;
			send_var_state = SEND_VAR_UNUSED;
			change_var_state = CHANGE_VAR_IDLE;

			break;
		}
	}
}

/*
 * Function: 		void evcal_changeVariable(void);
 * Description: 	receive new value of variable over uart then write to variable the new value
 * Parameters:		None
 * Return Value:	None
 */
void evcal_changeVariable(void)
{
	switch(change_var_state)
	{
		case CHANGE_VAR_IDLE:
		{
			//should never reach here
			break;
		}
		case CHANGE_VAR_START:
		{
			//create varID
			char varID[10] = "";
			//reset varID '\0'
			//memset(varID, '\0', sizeof(varID));

			//put length of ID in variable
			char tempConversionBuffer = uartMsgArr[1];
			lenID = charToInt(&tempConversionBuffer);

			//get varID moved out of uart message
			for(int i = 1; i < 1 + lenID; i++)
			{
				varID[i-1] = uartMsgArr[i+1];
			}

			//set id of variable
			address = charToInt(&varID[0]);

			//next set value length into variable
			tempConversionBuffer = uartMsgArr[5];
			valueLen = charToInt(&tempConversionBuffer);

			//next put value into value array before sending it to change the variable
			for(int i = 5; i < 5 + valueLen; i++)
			{
				valueArr[i-5] = uartMsgArr[i+1];
			}

			//get value from array and into variable
			value = charToInt(valueArrPtr);

			//set new value
			tracking_varSet(address, valuePtr);

			/*
			if(valueLen == 1)
			{
				valueArr[0] = uartMsgArr[6];
			}
			else if(valueLen == 2)
			{
				valueArr[0] = uartMsgArr[6];
				valueArr[1] = uartMsgArr[7];
			}
			else if(valueLen == 3)
			{
				valueArr[0] = uartMsgArr[6];
				valueArr[1] = uartMsgArr[7];
				valueArr[2] = uartMsgArr[8];
			}
			else if(valueLen == 4)
			{
				valueArr[0] = uartMsgArr[6];
				valueArr[1] = uartMsgArr[7];
				valueArr[2] = uartMsgArr[8];
				valueArr[3] = uartMsgArr[9];
			}
			else if(valueLen == 4)
			{
				valueArr[0] = uartMsgArr[6];
				valueArr[1] = uartMsgArr[7];
				valueArr[2] = uartMsgArr[8];
				valueArr[3] = uartMsgArr[9];
			}
			*/

			//old
			/*
			//no more values need to be pulled, now just fetch value of Variable and send back over uart.
			//get value and convert to char
			valueInt = tracking_varGet(address);
			//intToChar(valueInt, *valueArrPtr);
			sprintf(valueArr, "%d", valueInt);
			valueLen = getArrayFilledLength(valueArr, 10);
			valueLenChar = convertInt(valueLen); //convert to char

			//send to pc
			sendBuffer[0] = valueLenChar;
			for(int i = 1; i < 11; i++)
			{
				sendBuffer[i] = valueArr[i - 1];
			}
			*/

			change_var_state = CHANGE_VAR_DELAY;
			break;
		}
		case CHANGE_VAR_DELAY:
		{
			//send communication ack and reset states to unused
			//uint8_t theLen = getArrayFilledLength(sendBuffer, ELEVEN_BYTES);

			//uart_transmit(sendBufferPtr, theLen);

			//set states to unused state
			selected_command_state = NO_COMMAND;
			comm_check_state = COMM_CHECK_UNUSED;
			poll_state = WAITING_FOR_COMMAND;
			send_var_state = SEND_VAR_UNUSED;
			change_var_state = CHANGE_VAR_IDLE;

			//reset uartMsgArr '\0'
			memset(uartMsgArr, '\0', sizeof(uartMsgArr));
			//reset valueArr
			memset(valueArr, '\0', sizeof(valueArr));
			//reset sendBuffer
			memset(sendBuffer, '\0', sizeof(sendBuffer));

			int theNewValue = tracking_varGet(address);

			//address = 0;

			break;
		}
	}

	/*
	//char lenBufferChar[1];
	//char *lenBufferCharPtr = lenBufferChar;
	//char valueLenChar[1];
	//char *valueLenCharPtr = valueLenChar;

	uint8_t lenBufferChar = 0;
	//uint8_t *lenBufferCharPtr = &lenBufferChar;
	uint8_t valueLenChar = 0;
	//char *valueLenCharPtr = &valueLenChar;

	uint8_t lenID = 0;
	uint8_t valueLen = 0;
	char varID[10] = "";
	char *varIDPtr = varID;
	uint8_t address = 0;
	char valueArr[10];
	char *valueArrPtr = valueArr;
	int32_t value = 0;
	int32_t *valuePtr = &value;
	*/

	/*
	//delay because python slow
	while(uart_getReceiveCount()!= ONE_BYTE){}

	//receive length
	if(uart_getReceiveCount() == ONE_BYTE)
	{
		uart_receive(&lenBufferChar, ONE_BYTE);
		lenID = convertBack(lenBufferChar);

		//return value to test if accurately receive (debug only)
		//if(lenID != 0)
		//{
		//	//delay because python is slow
		//	for(int i = 0; i < 500; i++) {}
		//	//transmit value
		//	uart_transmit(lenBufferCharPtr, 1);
		//}


		//delay until buffer filled with proper length by slow python
		while(uart_getReceiveCount()!= lenID){}
		//receive the variable id for ptr array of variables and convert to int
		uart_receive(varIDPtr, lenID);
		address = charToInt(varIDPtr);

		//debug purposes
		//delay because python is slow
		for(int i = 0; i < 500; i++) {}
		uart_transmit(varIDPtr, lenID);

		//delay because python slow (length of value to change)
		while(uart_getReceiveCount()!= ONE_BYTE){}
		//get length of new value
		uart_receive(&valueLenChar, ONE_BYTE);
		valueLen = convertBack(valueLenChar); //get length of incoming value in next statement

		//get new value
		while(uart_getReceiveCount()!= valueLen){}
		uart_receive(valueArrPtr, valueLen);
		value = charToInt(valueArrPtr);

		//debug purposes
		//delay because python is slow
		for(int i = 0; i < 500; i++) {}
		uart_transmit(valueArrPtr, valueLen);

		// ****change variable****
		tracking_varSet(address, valuePtr);
	}
	selected_command_state = NO_COMMAND;
	*/
}

/*
 * Function: 		void evcal_sendVariable(void);
 * Description: 	get value of variable and send to pc over uart
 * Parameters:		None
 * Return Value:	None
 */
void evcal_sendVariable(void)
{
	switch(send_var_state)
	{
		case SEND_VAR_UNUSED:
		{
			//should never reach here
			break;
		}
		case SEND_VAR_START:
		{
			//create varID
			char varID[10] = "";

			//put length of ID in variable
			char tempConversionBuffer = uartMsgArr[1];
			lenID = charToInt(&tempConversionBuffer);

			//get varID moved out of uart message
			for(uint8_t i = 1; i < 1 + lenID; i++)
			{
				varID[i-1] = uartMsgArr[i+1];
			}

			/*
			if(lenID == 1)
			{
				varID[0] = uartMsgArr[2];
			}
			else if(lenID == 2)
			{
				varID[0] = uartMsgArr[2];
				varID[1] = uartMsgArr[3];
			}
			else if(lenID == 3)
			{
				varID[0] = uartMsgArr[2];
				varID[1] = uartMsgArr[3];
				varID[3] = uartMsgArr[4];
			}
			*/

			//set id of variable
			address = charToInt(&varID[0]);

			//no more values need to be pulled, now just fetch value of Variable and send back over uart.
			//get value and convert to char
			valueInt = tracking_varGet(address);
			//intToChar(valueInt, *valueArrPtr);
			sprintf(valueArr, "%d", valueInt);
			valueLen = getArrayFilledLength(valueArr, 10);
			valueLenChar = convertInt(valueLen); //convert to char

			//send to pc
			sendBuffer[0] = valueLenChar;
			for(int i = 1; i < 11; i++)
			{
				sendBuffer[i] = valueArr[i - 1];
			}

			send_var_state = SEND_VAR_DELAY;
			break;
		}
		case SEND_VAR_DELAY:
		{
			//send communication ack and reset states to unused
			uint8_t theLen = getArrayFilledLength(sendBuffer, ELEVEN_BYTES);

			uart_transmit(sendBufferPtr, theLen);

			//set states to unused state
			selected_command_state = NO_COMMAND;
			comm_check_state = COMM_CHECK_UNUSED;
			poll_state = WAITING_FOR_COMMAND;
			send_var_state = SEND_VAR_UNUSED;
			change_var_state = CHANGE_VAR_IDLE;


			//reset variables
			char resetArr[20];
			/*
			for(int i = 0; i < 20; i++)
			{
				resetArr[i] = "\0";
			}
			*/

			//uartMsgArr = "";

			//reset uartMsgArr '\0'
			memset(uartMsgArr, '\0', sizeof(uartMsgArr));
			//reset valueArr
			memset(valueArr, '\0', sizeof(valueArr));
			//reset sendBuffer
			memset(sendBuffer, '\0', sizeof(sendBuffer));

			/*
			//reset uartMsgArr
			for(int i = 0; i < 20; i++)
			{
				uartMsgArr[i] = resetArr[i];
			}

			//reset valueArr
			for(int i = 0; i < 10; i++)
			{
				valueArr[i] = resetArr[i];
			}

			//reset sendBuffer
			for(int i = 0; i < 11; i++)
			{
				sendBuffer[i] = resetArr[i];
			}
			*/


			/*
			sendBuffer[1] = 0;

			//empty buffer
			for(uint8_t i = 0; i < 11; i++)
			{
				&sendBuffer = "";
			}
			//empty buffer
			for(uint8_t i = 0; i < 10; i++)
			{
				*valueArr[i] = "";
			}

			//sendBuffer[] = "";
			*/

			break;
		}
	}


	/*
	//char lenBufferChar[1];
	//char *lenBufferCharPtr = lenBufferChar;
	//char valueLenChar[1];
	//char *valueLenCharPtr = valueLenChar;

	uint8_t lenBufferChar = 0;
	//char *lenBufferCharPtr = &lenBufferChar;
	uint8_t valueLenChar = 0;
	//char *valueLenCharPtr = &valueLenChar;

	uint8_t lenID = 0;
	uint8_t valueLen = 0;
	char varID[10] = "";
	char *varIDPtr = varID;
	uint8_t address = 0;
	char valueArr[10] = "";
	char *valueArrPtr = valueArr;
	//int value = 0;
	//int *valuePtr = &value;
	 */

	/*
	//delay because python slow
	while(uart_getReceiveCount()!= ONE_BYTE){}

	//receive length
	if(uart_getReceiveCount() == ONE_BYTE)
	{
		uart_receive(&lenBufferChar, ONE_BYTE);
		lenID = convertBack(lenBufferChar);

		//delay until buffer filled with proper length by slow python
		while(uart_getReceiveCount()!= lenID){}
		//receive the variable id for ptr array of variables and convert to int
		uart_receive(varIDPtr, lenID);
		address = charToInt(varIDPtr);

		//debug purposes check if id right
		//delay because python is slow
		for(int i = 0; i < 500; i++) {}
		uart_transmit(varIDPtr, lenID);

		//get address
		address = charToInt(varIDPtr);

		//get value and convert to char
		valueInt = tracking_varGet(address);
		//intToChar(valueInt, *valueArrPtr);
		sprintf(valueArr, "%d", valueInt);
		valueLen = getArrayFilledLength(valueArr, 10);
		valueLenChar = convertInt(valueLen); //convert to char

		//send length of value to pc
		for(int i = 0; i < 500; i++) {} //delay
		uart_transmit(&valueLenChar, ONE_BYTE);

		//send value to pc
		for(int i = 0; i < 500; i++) {} //delay
		uart_transmit(valueArrPtr, valueLen);

		//some kind of check process, send value to double check accuracy
		for(int i = 0; i < 500; i++) {} //delay
		uart_transmit(valueArrPtr, valueLen);
	} */
}

/*
 ******************************************************************************
 * Local FUNCTIONS
 ******************************************************************************
 */

/*
static void intToChar(int anInt, char *resultPtr)
{
    //create local buffer and reset to null
    char buffer[6] = "";

    //convert to char array
    sprintf(buffer, "%d", anInt);

    //set char array values to buffer
    for (int i = 0; i < 6; i++)
    {
        resultPtr[i] = buffer[i];
    }
}
*/

static int charToInt(char *charPtr)
{
    int result = 0;
    sscanf(charPtr, "%d", &result);
    return result;
}

static int charToHex(char *charPtr)
{
    //variable to return, reset to 0 each time.
    int result = 0;

    result = (int)strtol(charPtr, NULL, 16);

    return result;
}

static uint8_t convertBack(uint8_t aChar)
{
    char alphabet[] = " abcdefghijklmnopqrstuvwxyz"; //space is intentional
    int theInt;
    for(int i = 0; i < strlen(alphabet); i++)
    {
        if(alphabet[i] == aChar)
        {
            theInt = i;
        }
    }
    return theInt;
}

//only up to 26
static char convertInt(uint8_t anInt)
{
    char alphabet[] = " abcdefghijklmnopqrstuvwxyz"; //space is intentional

    char theChar = alphabet[anInt];

    return theChar;
}

int getArrayFilledLength(char array[], uint8_t length)
{
    int count = 0;

    for(int i = 0; i < length; i++)
    {
        if(array[i] != NULL)
        {
            count++;
        }
    }
    return count;
}
