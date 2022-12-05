#!/usr/bin/python3
"""
*******************************************************************************
      File Name  : gui.py
      Author     : jdyakimow
      Date       : 11/28/2022
      Description: gui for usdi fmstr
 ******************************************************************************
"""

"""
 ******************************************************************************
 * IMPORTS
 ******************************************************************************
"""

#library imports
import tkinter as tk
import pathlib
import pygubu

#file imports
import uart
import cmd

"""
 ******************************************************************************
 * VARIABLES and CONSTANTS
 ******************************************************************************
"""

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "usdi_fmstr.ui"
  
"""
 ******************************************************************************
 * FUNCTIONS
 ******************************************************************************
"""

#main application window
class UsdiFmstrApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel_main", master)

        self.labelValue_connectionStatus = None
        builder.import_variables(self, ['labelValue_connectionStatus'])

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_connect_btn_pressed(self):
        pass

    def on_disconnect_btn_pressed(self):
        pass

    def on_send_btn_pressed(self):
        pass
    
    #refresh all variables (access all variables on device)
    def on_refresh_btn_pressed(self):
        pass

"""
 * Function: 		example()
 * Description: 	example function
 * Parameters:		none
 * Return Value:	none
"""
def myExampleFunction():
  print("example function")