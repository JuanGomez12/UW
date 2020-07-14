# ECE 656 Project.
# Juan Manuel Gomez Gonzalez and Natalia Hoyos Velasquez


# The code for changing pages was derived from: 
#http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import mysql.connector
from tabulate import tabulate
import pandas as pd
verbose = 0

import os #Import os functions
dir_path = os.getcwd()
file_to_open = os.path.join(dir_path, "readme.txt")
try:
    with open(file_to_open, 'r') as file:
        readme_txt = file.read()
except:
    readme_txt = '\n\n Problem when opening the app: readme file not found. Make sure that it is in the same folder as the app'
    print('Readme file not found')

dispSize = 80
row_col_minSize = 40

class dbApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(False, False)
        container = tk.Frame(self)
        container.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'NSEW')
        container.rowconfigure(0, weight = 1)
        container.columnconfigure(0, weight = 1)
        
        self.frames = {}
        self.title("NB Classifier, J. M. Gomez and N. Hoyos")
            
        for F in (HomePage, StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            for i in range(11):
                if i == 7:
                    frame.rowconfigure(i, weight = 1)
                else:
                    frame.rowconfigure(i, weight = 1, minsize =  row_col_minSize)
            if F is StartPage:
                frame.grid(row = 0, column = 0, sticky = "nsew")
                frame.columnconfigure(0, weight = 1, minsize =  row_col_minSize)
            elif F is PageOne:
                frame.grid(row = 0, column = 0, sticky = "nsew")
                for i in range(3):
                    frame.columnconfigure(i, weight = 1, minsize = row_col_minSize)
            elif F is HomePage:
                frame.grid(row = 0, column = 0, sticky = "nsew")
#                 for i in range(2):
                frame.columnconfigure(0, weight = 1)
            else:
                frame.grid(row = 0, column = 0, sticky = "nsew")
                for i in range(3):
                    frame.columnconfigure(i, weight = 1)
        self.show_frame(HomePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        txt_introFrame = ttk.Frame(self, height = 4 * dispSize)
        txt_introFrame.columnconfigure(0, weight = 10)
        txt_intro = tk.Text(txt_introFrame, wrap = tk.WORD) #Create a text element  
        txt_intro.grid(row=0, column=0, sticky='NSEW')
        txtintro_scrollbar = ttk.Scrollbar(txt_introFrame, orient = tk.VERTICAL)
        txt_intro['yscrollcommand'] = txtintro_scrollbar.set
        txtintro_scrollbar.config(command = txt_intro.yview)
        txtintro_scrollbar.grid(row = 0, column = 1, sticky = 'NSEW')
        myFont = Font(family = "Calibri", size = 11)
        txt_intro.configure(font = myFont)
        
        txt = "ECE656 Winter 2019 Project,\n\nNatalia Hoyos Velasquez and Juan Manuel Gomez Gonzalez."
        txt = txt + readme_txt

        txt_intro.delete(1.0,tk.END)
        txt_intro.insert(tk.INSERT, txt)

        

        #Enter button
        btn_start = ttk.Button(self, text = 'Start', command = lambda: controller.show_frame(StartPage))
        #Exit button
        btn_exit = ttk.Button(self, text = 'Exit', command = controller.destroy)
        #Grid creation
        rowNum = 0
        #Margin
        #info
        txt_introFrame.grid(row = rowNum, column = 0, sticky = 'NSEW')
        
        
        #Button
        btn_start.grid(row = 2, column = 0, columnspan=2, sticky = 'NSEW')
        btn_exit.grid(row = 3, column = 0, columnspan=2, sticky = 'NSEW')
                    
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        loginFrame = ttk.Frame(self)
        l_conn = ttk.Label(loginFrame, text = "Connection:\n")
        l_user = ttk.Label(loginFrame, text = "DB user:\n") #Create a label element
        l_pswd = ttk.Label(loginFrame, text = "DB password:\n") #Create a label element
        l_db = ttk.Label(loginFrame, text = "DB to use:\n")
        e_conn = ttk.Entry(loginFrame)
        e_user = ttk.Entry(loginFrame) #Create an entry element
        e_pswd = ttk.Entry(loginFrame, show = "*") #Create an entry element
        e_db = ttk.Entry(loginFrame)
        
        #default values
        e_conn.delete(0, tk.END)
        e_user.delete(0, tk.END)
        e_pswd.delete(0, tk.END)
        e_db.delete(0, tk.END)
        
        e_conn.insert(0, "localhost")
        e_user.insert(0, "root")
#         e_pswd.insert(0, "a default value")
        e_db.insert(0, "ProjectNB")
        #end of default values
        
        txt_error_window = tk.Text(self, wrap = tk.WORD) #Create a text element
        #Create a button to run the dbConnect function on buttonpress:
        btn_enter = ttk.Button(self, text = 'Open DB', command = lambda: dbConnect())
        #Return button
        btn_return = ttk.Button(self, text = "Back to Home",
                            command = lambda: controller.show_frame(HomePage))
        
        #Grid creation
        rowNum = 0
        #host entry
        l_conn.grid(row = rowNum, column = 0, padx = 4, pady = 4, sticky = 'NSEW')
        e_conn.grid(row = rowNum, column = 1, padx = 4, pady = 4,  sticky = 'NSEW')
        rowNum = rowNum+1
        #User entry
        l_user.grid(row = rowNum, column = 0, padx = 4, pady = 4,  sticky = 'NSEW')
        e_user.grid(row = rowNum, column = 1, padx = 4, pady = 4,  sticky = 'NSEW')
        rowNum = rowNum+1
        #Password entry
        l_pswd.grid(row = rowNum, column = 0, padx = 4, pady = 4,  sticky = 'NSEW')
        e_pswd.grid(row = rowNum, column = 1, padx = 4, pady = 4,  sticky = 'NSEW')
        rowNum = rowNum+1
        #db entry
        l_db.grid(row = rowNum, column = 0, padx = 4, pady = 4,  sticky = 'NSEW')
        e_db.grid(row = rowNum, column = 1, padx = 4, pady = 4,  sticky = 'NSEW')
        #Info frame
        loginFrame.grid(row = 0, column = 0, padx = 4, pady = 4,  sticky = 'NSEW')
        loginFrame.grid_columnconfigure(0, weight = 0)
        loginFrame.grid_columnconfigure(1, weight = 1)
        txt_error_window.grid(row = 1, column = 0, padx = 4, pady = 4,  sticky = 'NSEW')
        
        #Enter button
        btn_enter.grid(row = 2, column = 0, sticky = 'SNEW')
        btn_return.grid(row = 3, column = 0, sticky = 'SNEW')
        
        def dbConnect():
            txt_error_window.delete(1.0, tk.END)
            try:
                global mydb 
                mydb = mysql.connector.connect(
                  host = e_conn.get(), #host
                  user = e_user.get(), #user
                  passwd = e_pswd.get(), #password
                  database = e_db.get() #database
                )
                mycursor = mydb.cursor()
                args = [e_db.get()]
                mycursor.callproc("GetDBName", args)
                mycursor.close()
                controller.show_frame(PageOne)
            except Exception as e:
                err = "Error connecting to db \n"
                err = err + "Check if there is an error with the connection name, user, password or database\n\n"
                err = err + "Error message: \n" + str(e)
                txt_error_window.insert(tk.INSERT,err)
                if verbose == 1:
                    print("Error connecting to db.")
                    print("Check if there is an error with the connection name, user, password or database")

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Text output creation and its scrollbar creation and placement
        txt_outputFrame = ttk.Frame(self, height = 1.5 * dispSize)
        txt_outputFrame.columnconfigure(0, weight = 10)
        txt_outputFrame.grid_propagate(False)
        txt_output = tk.Text(txt_outputFrame, wrap = tk.WORD) #Create a text element
        txt_output.tag_configure("center", justify = 'center')
        txt_output.grid(row = 0, column = 0, sticky = 'WE')
        
        txt_output.delete(1.0,tk.END)
        txt_output.insert(tk.INSERT, 'Connection established with server', "center")
        label_selectedTable = ttk.Label(self, text = '3. Select table to use:\n')
        
        # Feature ListBox creation and its scrollbar creation and placement
        LBoxframe_master = ttk.Frame(self)
        LBoxframe = ttk.Frame(LBoxframe_master)
        label_listbox =  ttk.Label(LBoxframe_master, text = '4. Variables to use for prediction')
        LBoxframe_master.grid_columnconfigure(0, weight = 0)
        LBoxframe_master.grid_columnconfigure(1, weight = 1)
        LBoxframe.grid(row = 0, column = 1, padx=4, sticky = 'NSEW')
        label_listbox.grid(row = 0, column = 0, padx = 4,sticky = 'NSEW')
        scrollbar = ttk.Scrollbar(LBoxframe, orient = tk.VERTICAL)
        listbox = tk.Listbox(LBoxframe, selectmode = tk.MULTIPLE, yscrollcommand = scrollbar.set,
                             exportselection = 0)
        scrollbar.config(command = listbox.yview)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        listbox.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        
        
        #Combobox creation
        label_combobox = ttk.Label(LBoxframe_master, text = '5. Percentage to use as train for\n   the split')
        trainTest_cbox = ttk.Combobox(LBoxframe_master, state = "readonly",
                                      values = ([x for x in range(10,100,10)]))
        label_combobox.grid(row = 1, column = 0, padx = 4, pady=4, sticky = 'NSEW')
        trainTest_cbox.grid(row = 1, column = 1, padx = 4, pady=4, sticky = 'NSEW')
        
        #Batting table button
        buttonBatting =  ttk.Button(self, text = "Batting Table",
                            command = lambda: pop_fea_lbox("Batting", txt_output))
        #Pitching table button
        buttonPitching =  ttk.Button(self, text = "Pitching Table",
                            command = lambda: pop_fea_lbox("Pitching", txt_output))
        #Managers table button
        buttonManager =  ttk.Button(self, text = "Managers Table",
                            command = lambda: pop_fea_lbox("Managers", txt_output))
        #Run program button
        buttonSQL =  ttk.Button(self, text = "6. Create Classifier",
                            command = lambda: lboxSQL(txt_output, listbox, trainTest_cbox))
        
        # Test Players ListBox creation and its scrollbar creation and placement
        LBoxframe_master_test = ttk.Frame(self)
        LBoxframe_test = ttk.Frame(LBoxframe_master_test)
        label_listbox_test =  ttk.Label(LBoxframe_master_test, text = '7. Players to use for prediction')
        LBoxframe_master_test.grid_columnconfigure(0, weight = 0)
        LBoxframe_master_test.grid_columnconfigure(1, weight = 1)
        LBoxframe_test.grid(row = 0, column = 1, padx = 4, sticky = 'NSEW')
        label_listbox_test.grid(row = 0, column = 0, padx = 4, sticky = 'NSEW')
        scrollbar_test = ttk.Scrollbar(LBoxframe_test, orient = tk.VERTICAL)
        listbox_test = tk.Listbox(LBoxframe_test, yscrollcommand = scrollbar_test.set,
                             exportselection = 0)
        scrollbar_test.config(command = listbox_test.yview)
        scrollbar_test.pack(side = tk.RIGHT, fill = tk.Y)
        listbox_test.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        
        # Test players textbox creation and its scrollbar creation and placement
        txt_output_testFrame = ttk.Frame(self, height = dispSize)
        txt_output_testFrame.columnconfigure(0, weight = 10)
        txt_output_testFrame.grid_propagate(False)
        txt_output_test = tk.Text(txt_output_testFrame, wrap=tk.NONE) #Create a text element  
        txt_output_test.tag_configure("center", justify = 'center')
        txtscrollbar_test = ttk.Scrollbar(self, orient = tk.HORIZONTAL)
        txt_output_test['xscrollcommand'] = txtscrollbar_test.set
        txtscrollbar_test.config(command = txt_output_test.xview)
        
        txt_output_test.grid(row = 1, column = 0, columnspan = 3, sticky='WE')


        def onselect(evt):
            txt_res.delete(1.0,tk.END)
            txt_pred.delete(1.0,tk.END)
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            args = [value]
            mycursor = mydb.cursor()
            mycursor.callproc("GetTestData", args)
            for result in mycursor.stored_results():
                myresultColNames = result.column_names
                myresult = result.fetchall()
            #Convert the result into a DF
            df_result = pd.DataFrame(myresult, columns = myresultColNames)
            df_result = df_result.sort_values(df_result.columns[0], ascending = True)
            mycursor.close()
            if verbose == 1:
                print('For the player selection you selected item %d: "%s"' %(index, value))
            txt_output_test.delete(1.0,tk.END)
            niceTable = tabulate(df_result, headers = 'keys', tablefmt = 'psql')
            if len(niceTable) < 400:
                txt_output_test.insert(tk.INSERT, niceTable, "center")
            else:
                txt_output_test.insert(tk.INSERT, niceTable)
            
        listbox_test.bind('<<ListboxSelect>>', onselect)
        
        #Calculate Prediction and Class button
        buttonPredRes =  ttk.Button(self, text = "8. Predict Class",
                                    command = lambda: predClass())
        
        #PredictionResults frame
        predResFrame = ttk.Frame(self)
        predResFrame.columnconfigure(0, weight = 1)
        predResFrame.columnconfigure(1, weight = 1)
        predFrame = ttk.Frame(predResFrame)
        predFrame.columnconfigure(0, weight = 1)
        predFrame.grid(row = 0, column = 0, sticky = 'NSEW')
        pred_label = ttk.Label(predFrame, text = 'Predicted Value:')
        pred_label.grid(row = 0, column = 0)
        
        txt_predFrame = ttk.Frame(predFrame, height = dispSize)
        txt_predFrame.columnconfigure(0, weight = 1)
        txt_predFrame.grid_propagate(False)
        txt_pred = tk.Text(txt_predFrame, wrap = tk.WORD) #Create a text element
        txt_pred.tag_configure("center", justify = 'center')
        txt_pred.grid(row = 0, column = 0, sticky = 'WE')
        
        txt_predFrame.grid(row=1, column=0, sticky = 'NSEW')
        
        resFrame = ttk.Frame(predResFrame)
        resFrame.columnconfigure(0, weight = 1)
        resFrame.grid(row=0, column=1, sticky = 'NSEW')
        res_label = ttk.Label(resFrame, text = 'Real Value:')
        res_label.grid(row=0, column=0)
        
        txt_resFrame = ttk.Frame(resFrame, height = dispSize)
        txt_resFrame.columnconfigure(0, weight=1)
        txt_resFrame.grid_propagate(False)
        txt_res = tk.Text(txt_resFrame, wrap = tk.WORD) #Create a text element
        txt_res.tag_configure("center", justify = 'center')
        txt_res.grid(row = 0, column = 0, sticky = 'WE')

        txt_resFrame.grid(row=1, column=0, sticky = 'NSEW')
        
        #Return button button
        button1 = ttk.Button(self, text = "Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        
        #Place table selection buttons
        label_selectedTable.grid(row = 0, column = 0, columnspan = 3, padx = 4, pady = 4, sticky = 'WNSE')
        buttonBatting.grid(row = 1, column = 0, pady = 4, sticky = 'NSEW')
        buttonPitching.grid(row = 1, column = 1, pady = 4, sticky = 'NSEW')
        buttonManager.grid(row = 1, column = 2, pady = 4, sticky = 'NSEW')
        
        #Place listbox and combobox frame
        LBoxframe_master.grid(row = 2, column = 0, columnspan = 3, padx = 4, pady = 4, sticky = 'NSEW')
        
        #Place run button
        buttonSQL.grid(row = 3, column = 0, columnspan = 3, padx = 4, pady = 4, sticky = 'NSEW')
        
        #Place output textbox
        txt_outputFrame.grid(row = 4, column = 0, columnspan = 3, padx = 4, pady = 4, sticky = 'NSEW')
        
        #Place test listbox and combobox frame
        LBoxframe_master_test.grid(row = 5, column = 0, columnspan = 3, padx = 4, pady = 4, sticky = 'NSEW')
        
        #Place test textbox frame and scrollbar
        txt_output_testFrame.grid(row = 6, column = 0, columnspan = 3, padx = 4, sticky = 'NSEW')
        txtscrollbar_test.grid(row = 7, column = 0, columnspan = 3, padx = 4, sticky = 'NSEW')
        
        #Place button
        buttonPredRes.grid(row = 8, column = 0, columnspan = 3, padx = 4, pady = 4, sticky = 'NSEW')
        
        #Predicted and results frame
        predResFrame.grid(row = 9, column = 0, columnspan = 3, padx = 4, pady = 4, sticky = 'NSEW')
        
        #Place return button
        button1.grid(row = 10, column = 0, columnspan = 3, padx = 4, pady = 4, sticky = 'NSEW')
        
        def pop_fea_lbox(table, textOutput): #Populate Feature Listbox
            # Clean all tables of text
            txt_res.delete(1.0,tk.END)
            txt_pred.delete(1.0,tk.END)
            txt_output_test.delete(1.0,tk.END)
            listbox_test.delete(0,tk.END) #When table button is pressed
            #Populates the listbox according to the table selected as input
            #Create the cursor
            mycursor = mydb.cursor()
            #Create a global variable with the table used for the current analysis
            global selected_table
            selected_table = table
            #Print a message to the user
            textOutput.delete(1.0,tk.END)
            textOutput.insert(tk.INSERT, table + ' table selected', 'center')
            listbox.delete(0,tk.END)
            #Call the columnIdentifier procedure from the DB server
            args = [table]
            mycursor.callproc("columnIdentifier", args)
            colNames = mycursor.column_names
            for result in mycursor.stored_results():
                myresult = result.fetchall()
            mycursor.close()
            #Convert the result into a DF
            df_result = pd.DataFrame(myresult, columns = colNames)
            df_result = df_result.sort_values(df_result.columns[0], ascending = True)
            #Insert the data into the listbox
            listbox.delete(0,tk.END)
            for i in range(len(df_result)):
                if verbose == 1: #Print results to output if verbose = 1
                    print("Listbox value: " + df_result.iloc[i,0])
                if not df_result.iloc[i,0] == "playerID":
                    listbox.insert(tk.END, df_result.iloc[i,0])
               
        def lboxSQL(textOutput, lbox, cbox):
            txt_res.delete(1.0,tk.END)
            txt_pred.delete(1.0,tk.END)
            txt_output_test.delete(1.0,tk.END)
            #Get the listbox's current selection
            items = lbox.curselection()
            # Get the currently selected percentage
            cbox_percentage = cbox.get()
            #Convert the percentage into the decimal equivalent, if there was a selection
            if cbox_percentage == "":
                cbox_percentage = -1
            else:
                cbox_percentage = float(cbox_percentage)/100
            if verbose == 1:
                print("Train-Test Percentage: %3.1f" %(cbox_percentage))
            #Check if there was a percentage selected
            if cbox_percentage > 0:
                #Check if there were any items selected from the listbox
                num_selected_features = len(items)
                if num_selected_features > 0:
                    if verbose == 1:
                        print(num_selected_features) #Print the number of items picked by the user
                    #Create the cursor
                    mycursor = mydb.cursor()
                    #Create a string to save all the selected items from the listbox, separated by a space
                    x = 0
                    for item in items:
                        if x > 0:
                            featuresString = featuresString + "` `" + lbox.get(item)
                            fString_nice = fString_nice + ', ' + lbox.get(item)
                        else:
                            featuresString = "`" + lbox.get(item)
                            fString_nice = lbox.get(item)
                        x = x + 1
                    featuresString = featuresString + "`"
                    dispText = 'Creating the classifier using the table ' + selected_table 
                    dispText = dispText + ' and using the features: ' + fString_nice
                    textOutput.delete(1.0,tk.END)
                    textOutput.insert(tk.INSERT, dispText, 'center')
                    if verbose == 1:
                        print(featuresString) #Print the string
                    # Call the MasterProcedure stored procedure from the DB Server
                    args = [featuresString, cbox_percentage]
                    mycursor.callproc("MasterProcedure", args)
                    for result in mycursor.stored_results():
                        if verbose == 1:
                            print(result.description)
                        myresult = result.fetchall()
                        resultCursor = result
                    mycursor.close()
                    if verbose == 1:
                        print(resultCursor.column_names)
                    #Convert to a DF
                    df_result = pd.DataFrame(myresult, columns = resultCursor.column_names)
                    df_result = df_result.sort_values(df_result.columns[0], ascending = True)
                    textOutput.delete(1.0,tk.END)
                    textOutput.insert(tk.INSERT, tabulate(df_result, headers = 'keys', tablefmt = 'psql'),
                                      'center')
                    #Obtain the test variables
                    mycursor = mydb.cursor()
                    mycursor.callproc("GetTest")
                    for result in mycursor.stored_results():
                        myresult = result.fetchall()
                        if verbose == 1:
                            print("List of test players found")
                            print(myresult)
                    mycursor.close()
                    #Convert the result into a DF
                    df_result = pd.DataFrame(myresult)
                    #Insert the data into the test listbox
                    listbox_test.delete(0,tk.END)
                    for i in range(len(df_result)):
                        if verbose == 1: #Print results to output if verbose = 1
                            print("Listbox value: " + df_result.iloc[i,0])
                        listbox_test.insert(tk.END, df_result.iloc[i,0])
                else:
                    textOutput.delete(1.0,tk.END)
                    textOutput.insert(tk.INSERT, "No fields selected to create the prediction algorithm",
                                      'center')
            else:
                textOutput.delete(1.0,tk.END)
                textOutput.insert(tk.INSERT, "Please select a percentage value for the train-test split",
                                  'center')  
            return

        def predClass():
            index = int(listbox_test.curselection()[0])
            value = listbox_test.get(index)
            ## Predicted calculation
            args = [value , 'predicted']
            mycursor = mydb.cursor()
            mycursor.callproc("GetClass", args)
            for result in mycursor.stored_results():
                myresultColNames = result.column_names
                myresult = result.fetchall()
            # Convert the result into a DF
            df_result = pd.DataFrame(myresult, columns = myresultColNames)
            mycursor.close()
            txt_pred.delete(1.0,tk.END)
            txt_pred.insert(tk.INSERT, tabulate(df_result, headers = 'keys', tablefmt = 'psql'), "center")
            ## Real value calculation
            args = [value , 'candidate']
            mycursor = mydb.cursor()
            mycursor.callproc("GetClass", args)
            for result in mycursor.stored_results():
                myresultColNames = result.column_names
                myresult = result.fetchall()
            # Convert the result into a DF
            df_result = pd.DataFrame(myresult, columns = myresultColNames)
            mycursor.close()
            txt_res.delete(1.0,tk.END)
            txt_res.insert(tk.INSERT, tabulate(df_result, headers = 'keys', tablefmt = 'psql'), "center")
        
app = dbApp()
app.mainloop()
