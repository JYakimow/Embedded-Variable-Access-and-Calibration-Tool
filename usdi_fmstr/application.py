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
from ast import Delete
import tkinter as tk
from tkinter import END, ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import *
import pathlib
import pygubu
import datetime
import logging
import os

#file imports
import uart
import command
import debug_logging as log

"""
 ******************************************************************************
 * VARIABLES and CONSTANTS
 ******************************************************************************
"""

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "usdi_fmstr.ui"
  
"""
 ******************************************************************************
 * FUNCTIONS and CLASSES
 ******************************************************************************
"""

#main application window
class UsdiFmstrApp:
    connection_status = False
    comPortList = list()
    varArrayLength = int()

    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel_main", master)
      
        self.labelValue_connectionStatus = None
        builder.import_variables(self, ['labelValue_connectionStatus'])

        builder.connect_callbacks(self)

        self.mainwindow.protocol("WM_DELETE_WINDOW",  self.on_close)

        #init object access
        self.label_connectionStatus = builder.get_object("label_connectionStatus")
        self.comboBox_comPort = builder.get_object("comboBox_comPort")
        self.comboBox_baud = builder.get_object("comboBox_baudRate")
        self.comboBox_dataBits = builder.get_object("comboBox_dataBits")
        self.comboBox_variableID = builder.get_object("comboBox_variableID")
        self.entry_newValue = builder.get_object("entry_newValue")
        self.comboBox_stopBits = builder.get_object("comboBox_stopBits")
        self.comboBox_parityBit = builder.get_object("comboBox_parityBit")
        

        #******configure treeview to display right amount of columns******
        self.tree_varDisplay = builder.get_object("treeview_varData")
        self.tree_varDisplay.column("#0", width=0, stretch = "no") #hide empty first column
        #self.tree_varDisplay.heading("#0", text="")
        self.add_columns(("Variable ID", "Value"))
        self.tree_varDisplay.column("#1", width=0, anchor=tk.CENTER)
        self.tree_varDisplay.column("#2", width=0, anchor=tk.CENTER)
        #anchor=tk.CENTER

        #detect avalible com ports and load to com port combobox
        self.getComPorts()
        #load number of vars
        self.loadVarNum()

        """
        id = self.tree_varDisplay.insert('', 'end', iid="id_1", text="1", values=("<id num>", "<value>"))
        print(id)
        #self.tree_varDisplay.insert('', 'end', )
        #self.tree_varDisplay.set('Variable ID', '1', 'page')
        #self.tree_varDisplay.item("1", values=("1", "page"))
        #self.tree_varDisplay.set("id_1", column="Value", value="new val")
        anInt = 1
        idVal = "id_" + str(anInt)
        x = self.tree_varDisplay.item(idVal)["values"][1] #get value to be changed
        print(x)"""
    
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
        #print(datetime.datetime.now(), "LOG: Application launched\n")
        log.info("Application launched")
        self.mainwindow.mainloop()

    def on_connect_btn_pressed(self):
        try:
            uart.init(self.comboBox_comPort.get(), 
                      self.comboBox_baud.get(),
                      self.comboBox_dataBits.get(),
                      self.comboBox_stopBits.get(),
                      self.comboBox_parityBit.get())
            self.labelValue_connectionStatus.set("Connected")
            self.connection_status = True
            if(command.testConnection() == False):
                uart.closeConnection()
                log.warning("Connection settings not properly configured for communication.")
                log.info("COM port closed")
                tk.messagebox.showwarning(title="Warning", message="WARNING: Connection settings not properly configured for communication.")
        except Exception as ex:
            log.error(ex)
            log.error("UART connection settings must be selected in order to open connection")
            tk.messagebox.showerror(title="Error", message="UART connection settings must be selected in order to open connection")

    def on_disconnect_btn_pressed(self):
        try:
            if(self.connection_status == True):
                uart.ser.close()
                self.labelValue_connectionStatus.set("Disconnected")
                log.info("COM port closed")
                self.connection_status = False
            else:
                log.error("No connection to terminate")
                tk.messagebox.showwarning(title="Alert", message="No connection to terminate")
        except Exception as ex:
            log.error(ex)
            tk.messagebox.showerror(title="Error", message=ex)

    def on_send_btn_pressed(self):
        try:
            #send change variable command
            command.changeVariable(int(self.entry_newValue.get()), int(self.comboBox_variableID.get()))

            #refresh the variable displayed
            idVal = "id_" + str(self.comboBox_variableID.get())
            self.tree_varDisplay.set(idVal, column="Value", value=str(self.entry_newValue.get()))

            #clear entry widget
            self.entry_newValue.delete(0, END)
        except Exception as ex:
            log.error(ex)
            tk.messagebox.showerror(title="Error", message=ex)
    
    #refresh all variables (access all variables on device)
    def on_refresh_btn_pressed(self):
        try:
            if(self.connection_status == True):
                #clear existing
                for item in self.tree_varDisplay.get_children():
                    self.tree_varDisplay.delete(item)
                #aString1 = 'test'
                for i in range(command.CAL_ARRAY_LENGTH):
                    try:
                        idVal = "id_" + str(i+1)
                        varValue = command.getVariable(i + 1) #.decode("ascii")    
                        #print("Value of variable", i, "is", a)
                        #aString1new = aString1 + str(i)
                        self.tree_varDisplay.insert('', 'end', iid=idVal, text="1", values=(i+1, varValue))
                    except Exception as ex:
                        self.tree_varDisplay.insert('', 'end', text="1", values=(i+1, "error"))
                        log.error(ex)
                        #tk.messagebox.showerror(message=ex)
            else:
                tk.messagebox.showwarning(title="Warning", message="Alert: COM port not open")
                log.error("COM port not open exception")
                #print(datetime.datetime.now(), "LOG: Alert: COM port not open exception\n")
        except Exception as ex:
            log.error(ex)
            tk.messagebox.showerror(title="Error", message=ex)

    def on_load_btn_pressed(self):
        try:
            #empty treeview
            for item in self.tree_varDisplay.get_children():
                self.tree_varDisplay.delete(item)

            #load file
            theFile = filedialog.askopenfile()
            contents = theFile.read()

            resultList = contents.split("!")
            self.varArrayLength = int(resultList[0])
            #print(self.varArrayLength)
            resultList = resultList[1].split(";")
            #print(resultList)

            buffer = list()
            for i in range(self.varArrayLength):
                buffer = resultList[i].split(":")
                command.changeVariable(buffer[1], buffer[0])
                idVal = "id_" + str(i+1)
                self.tree_varDisplay.insert('', 'end', iid=idVal, text="1", values=(buffer[0], buffer[1]))
                """
                try:
                    command.changeVariable(buffer[1], buffer[0])
                except Exception as ex:
                    #log.error("UART Communication Error")
                    #tk.messagebox.showerror(title="Error", message="UART Communication Error")
                    log.error(ex)
                    tk.messagebox.showerror(title="Error", message=ex)
                """

        except Exception as ex:
            log.error(ex)
            tk.messagebox.showerror(title="Error", message=ex)

    def on_save_btn_pressed(self):
        try:
            files = [('Variable Profile', '*.var-profile')]
            theFileID = asksaveasfile(initialdir = os.getcwd() + "\profiles", filetypes = files, defaultextension = files)
            #print(theFileID)
            outputList = list()
            outputList.append(str(command.CAL_ARRAY_LENGTH) + "!")
            for i in range(command.CAL_ARRAY_LENGTH):
                idVal = "id_" + str(i+1)
                value = self.tree_varDisplay.item(idVal)["values"][1]
                theId = self.tree_varDisplay.item(idVal)["values"][0]
                if(value == None):
                    outputList.append(str(theId) + ":" + "None" + ";")
                else:
                    outputList.append(str(theId) + ":" + str(value) + ";")
            theFileID.writelines(outputList)
        except Exception as ex:
            log.error(ex)
            tk.messagebox.showerror(title="Error", message=ex)

    def getComPorts(self):
        try:
            self.comPortList = uart.getPorts()
            cache = list()
            for i in self.comPortList:
                cache.append(i)
            #self.comboBox_comPort['state'] = 'readonly' #other options are 'normal' or 'disabled'
            self.comboBox_comPort['values'] = cache
        except Exception as ex:
            log.error(ex)
            tk.messagebox.showerror(title="Error", message=ex)

    def loadVarNum(self):
        #self.comPortList = uart.getPorts()
        cache = list()
        for i in range(command.CAL_ARRAY_LENGTH):
            cache.append(i+1)
        #self.comboBox_comPort['state'] = 'readonly' #other options are 'normal' or 'disabled'
        self.comboBox_variableID['values'] = cache

    def on_close(self):
        #print(datetime.datetime.now(), "LOG: Application closed")
        log.info("Application closed")
        self.mainwindow.destroy()

"""
 * Function: 		example()
 * Description: 	example function
 * Parameters:		none
 * Return Value:	none
"""
def myExampleFunction():
  print("example function")