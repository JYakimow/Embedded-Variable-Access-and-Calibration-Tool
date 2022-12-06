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
from tkinter import ttk
from tkinter import messagebox
import pathlib
import pygubu
import datetime

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
    connection_status = False
    comPortList = list()

    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel_main", master)
      
        self.labelValue_connectionStatus = None
        builder.import_variables(self, ['labelValue_connectionStatus'])

        builder.connect_callbacks(self)

        #init values to track
        self.label_connectionStatus = builder.get_object("label_connectionStatus")
        self.comboBox_comPort = builder.get_object("comboBox_comPort")
        self.comboBox_baud = builder.get_object("comboBox_baudRate")
        self.comboBox_dataBits = builder.get_object("comboBox_dataBits")
        self.comboBox_variableID = builder.get_object("comboBox_variableID")
        self.entry_newValue = builder.get_object("entry_newValue")
        

        #******configure treeview to display right amount of columns******
        self.tree_varDisplay = builder.get_object("treeview_varData")
        self.tree_varDisplay.column("#0", width=0, stretch = "no") #hide empty first column
        #self.tree_varDisplay.heading("#0", text="")
        self.add_columns(("Variable ID", "Value"))


        self.tree_varDisplay.column("#1", width=0, anchor=tk.CENTER)
        self.tree_varDisplay.column("#2", width=0, anchor=tk.CENTER)
        #anchor=CENTER

        #detect avalible com ports and load to com port combobox
        self.getComPorts()
        #load number of vars
        self.loadVarNum()
    
    def add_columns(self, columns, **kwargs): #**kwargs *args
        # Preserve current column headers and their settings
        current_columns = list(self.tree_varDisplay['columns'])
        current_columns = {key:self.tree_varDisplay.heading(key) for key in current_columns}

        # Update with new columns
        self.tree_varDisplay['columns'] = list(current_columns.keys()) + list(columns)
        for key in columns:
            self.tree_varDisplay.heading(key, text=key, **kwargs)
        
        # Set saved column values for the already existing columns
        for key in current_columns:
            # State is not valid to set with heading
            state = current_columns[key].pop('state')
            self.tree_varDisplay.heading(key, **current_columns[key])

    def run(self):
        #self.mainwindow.eval('tk::PlaceWindow . center')
        print(datetime.datetime.now(), "LOG: Application launched\n")
        self.mainwindow.mainloop()

    def on_connect_btn_pressed(self):
        try:
            uart.init(self.comboBox_comPort.get(), 
                      self.comboBox_baud.get(),
                      self.comboBox_dataBits.get())
            self.labelValue_connectionStatus.set("Connected")
            self.connection_status = True
        except Exception as ex:
            print(datetime.datetime.now(), "LOG:", ex, "\n")
            tk.messagebox.showerror(title="Error", message=ex)

    def on_disconnect_btn_pressed(self):
        try:
            if(self.connection_status == True):
                uart.ser.close()
                self.labelValue_connectionStatus.set("Disconnected")
                print(datetime.datetime.now(), "LOG: COM port closed\n")
                self.connection_status = False
            else:
                print(datetime.datetime.now(), "LOG: Error: No connection to terminate\n")
                tk.messagebox.showwarning(title="Alert", message="No connection to terminate")
        except Exception as ex:
            print(datetime.datetime.now(), "LOG:", ex, "\n")
            tk.messagebox.showerror(title="Error", message=ex)
            self.comboBox_comPort


    def on_send_btn_pressed(self):
        self.comboBox_variableID
        self.entry_newValue
        cmd.changeVariable(int(self.entry_newValue.get()), int(self.comboBox_variableID.get()))

        #refresh that variable
        varValue = cmd.getVariable(int(self.comboBox_variableID.get())).decode("ascii")
        self.tree_varDisplay.insert('', 'end', text="1", values=(int(self.comboBox_variableID.get()), varValue))
    
    #refresh all variables (access all variables on device)
    def on_refresh_btn_pressed(self):
        try:
            #aString1 = 'test'
            for i in range(cmd.CAL_ARRAY_LENGTH):
                try:
                    varValue = cmd.getVariable(i + 1).decode("ascii")    
                    #print("Value of variable", i, "is", a)
                    #aString1new = aString1 + str(i)
                    self.tree_varDisplay.insert('', 'end', text="1", values=(i+1, varValue))
                except Exception as ex:
                    self.tree_varDisplay.insert('', 'end', text="1", values=(i+1, "error"))
                    print(datetime.datetime.now(), "LOG: Error:", ex, "\n")
                    tk.messagebox.showerror(title="Error", message=ex)
                    self.comboBox_comPort
        except Exception as ex:
            print(datetime.datetime.now(), "LOG: Error:", ex, "\n")
            tk.messagebox.showerror(title="Error", message=ex)
            self.comboBox_comPort

    def getComPorts(self):
        self.comPortList = uart.getPorts()
        cache = list()
        for i in self.comPortList:
            cache.append(i)
        #self.comboBox_comPort['state'] = 'readonly' #other options are 'normal' or 'disabled'
        self.comboBox_comPort['values'] = cache

    def loadVarNum(self):
        #self.comPortList = uart.getPorts()
        cache = list()
        for i in range(cmd.CAL_ARRAY_LENGTH):
            cache.append(i+1)
        #self.comboBox_comPort['state'] = 'readonly' #other options are 'normal' or 'disabled'
        self.comboBox_variableID['values'] = cache


"""
 * Function: 		example()
 * Description: 	example function
 * Parameters:		none
 * Return Value:	none
"""
def myExampleFunction():
  print("example function")