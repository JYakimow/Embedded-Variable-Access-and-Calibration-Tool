"""
*******************************************************************************
      File Name  : debug_logging.py
      Author     : jdyak
      Date       : 12/7/2022
      Description: logging functionality for usdi embedded variable access and calibration tool
 ******************************************************************************
"""

"""
 ******************************************************************************
 * IMPORTS
 ******************************************************************************
"""

#library imports
import logging
import datetime

#file imports


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

# create logger
logger = logging.getLogger("logging_tryout2")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
#name = str(datetime.datetime.now()) + ".log"
logging.basicConfig(filename="runtime.log", filemode='w', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
#logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')

# add formatter to ch
consoleHandler.setFormatter(formatter)

# add ch to logger
logger.addHandler(consoleHandler)

"""
 * Function: 		debug(message)
 * Description: 	send logger message of type: debug
 * Parameters:		message = string message value
 * Return Value:	None
"""
def debug(message):
    logger.debug(message)

"""
 * Function: 		info(message)
 * Description: 	send logger message of type: info
 * Parameters:		message = string message value
 * Return Value:	None
"""
def info(message):
    logger.info(message)

"""
 * Function: 		warning(message)
 * Description: 	send logger message of type: warning
 * Parameters:		message = string message value
 * Return Value:	None
"""
def warning(message):
    logger.warning(message)

"""
 * Function: 		error(message)
 * Description: 	send logger message of type: error
 * Parameters:		message = string message value
 * Return Value:	None
"""
def error(message):
    logger.error(message)

"""
 * Function: 		critical(message)
 * Description: 	send logger message of type: critical
 * Parameters:		message = string message value
 * Return Value:	None
"""
def critical(message):
    logger.critical(message)