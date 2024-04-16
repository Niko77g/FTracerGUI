from tkinter import *
import sqlite3
import datetime
from classOOP import Data
import os, sys

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

db_path = resource_path("trening_results.db") # vyuzitie funkcie resource_path pre vytvorenie .exe suboru k pristupu k databaze sqlite.
root = Tk()
root.resizable(False, False) # Zabrani maximalizovaniu GUI aplikacies
root.title("FTracer")  # nastavi hlavičku tkinter GUI na text:"FTracer"

def create_table():    # Funkcia create_table služí na vytvorenie databazovej tabulky so stlpcami ID, DATE, TIME, EXERCISE, NUMBER_OF_REPETITIONS, NUMBER_OF_SERIES, WEIGHT
    connection = sqlite3.connect(db_path)  # Prikaz sluzi na spojenie python programom a s sqlite3 databazou trening_results
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS trening_results("  # execute vytvara databazovu sqlite3 tabulku, alebo upravuje databzovu tabulku sqlite3
                   "id integer PRIMARY KEY AUTOINCREMENT,"
                   "date integer,"
                   "time integer,"
                   "exercise text,"
                   "number_of_repetitions integer,"
                   "number_of_series integer,"
                   "weight float)")
    connection.commit() # Uklada zmeni v sqlite3
    connection.close() # Ukoncuje spojenie z databazou sqlite3

def add_fun():  # Funkcia add_fun pridava nove zaznamy do databazy 
    global add_frame, exerciseEntry, number_of_repetitionsEntry, number_of_seriesEntry, weightEntry # Definovanie globalnych premien pre vyuzitie v podfunkciach 
    add_frame = Frame(root) # Vytvorenie noveho widgedu v GUI aplikacie s nazvom add_frame
    add_frame.grid(row=0,column=0, sticky="nsew") # Umoznuje widget roztiahnut po vsetkych smeroch podla hlavneho widgedu 

    exercise = Label(add_frame,text="Enter the name of the exercise you want to enter:", width=43, height=2,font=("TkHeadingFont",12))
    exercise.grid(row=1,column=0,padx=20,pady=1)
    exerciseEntry = Entry(add_frame, width=25) # Vytvori widget vstupneho polia so sirkou 25 px
    exerciseEntry.grid(row=2,column=0,padx=20,pady=1) # Umiestnenie widgetu vstupneho polia do druheho riakdu a odstupom 20px podla x osi

    number_of_repetitions = Label(add_frame, text="Enter the number of repetitions:", width=33, height=2,font=("TkHeadingFont",12))
    number_of_repetitions.grid(row=3, column=0,padx=20,pady=1)
    number_of_repetitionsEntry = Entry(add_frame, width=25)
    number_of_repetitionsEntry.grid(row=4,column=0,padx=20,pady=1)
    number_of_series = Label(add_frame, text="Enter the number of series:", width=33, height=2,font=("TkHeadingFont",12))
    number_of_series.grid(row=5,column=0,padx=20,pady=1)
    number_of_seriesEntry = Entry(add_frame, width=25)
    number_of_seriesEntry.grid(row=6,column=0,padx=20,pady=1)
    weight = Label(add_frame, text="Enter the weight in kg:", width=33, height=2,font=("TkHeadingFont",12))
    weight.grid(row=7,column=0,padx=20,pady=1)
    weightEntry = Entry(add_frame, width=25)
    weightEntry.grid(row=8,column=0,padx=20,pady=1)
    # Vytvori tlacidlo, ktore po stlaceni spusti funkciu writefun a nastavi sirku a vysku tlacidla na 17 a 1. Zmeni font na 12 velkost
    submitadd = Button(add_frame,text="Add to the database",command=writefun,width=17, height=1,font=("TkHeadingFont",12), cursor="hand2") 
    submitadd.grid(row=9,column=0,padx=20,pady=7) # Nastavi rozlozenie tlacidla 
    BackButtonADD = Button(add_frame, text="Home", command=backmenu, cursor="hand2",width=17, height=1,font=("TkHeadingFont",12))
    BackButtonADD.grid(row=10,column=0,padx=20,pady=7)

def backmenu(): # Funkcia backmenu sluzi na odstranenie wdigetu add_frame a vratenie hlavneho widgetu frame1
    create_table()
    add_frame.grid_remove()
    frame1.tkraise()
def writefun():
    date = datetime.datetime.now().strftime("%m/%d/%Y") # Vytvorena premenna date, ktora obsahuje aktualny datum vo formate MM/DD/YYYY
    time = datetime.datetime.now().strftime("%H:%M") # Vytvorena premenna time, ktora obsahuje aktualny cas vo formate 24 hod.: HH/MM 
    exercise = exerciseEntry.get() # Ziska data exercise zo vstupu od uzivetala
    
    try: # try except vynimky sluzia na overenie spravne zadanych parametrov od uzivatela
        number_of_repetitions = int(number_of_repetitionsEntry.get())
        number_of_series = int(number_of_seriesEntry.get())
    except ValueError:
        erroradd = Label(add_frame,text="The value for the number of sets and reps must be a whole number!")
        erroradd.grid()
        return
    try:
        weight = float(weightEntry.get())
    except ValueError:
        error2add = Label(add_frame,text="The value for the weight must be in float or int format!")
        error2add.grid()
        return
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS trening_results(" # Vytvori databazovu tabulku v sqlite3 pokial este nie je
                   "id integer PRIMARY KEY AUTOINCREMENT,"
                   "date integer,"
                   "time integer,"
                   "exercise text,"
                   "number_of_repetitions integer,"
                   "number_of_series integer,"
                   "weight float)") 
    cursor.execute("INSERT INTO trening_results("  # Prida ziskane udaje od uzivatelov do databazovych tabuliek
                   "date,time,exercise,number_of_repetitions,"
                   "number_of_series, weight) VALUES (?,?,?,?,?,?)", 
                   (date, time, exercise, number_of_repetitions, number_of_series, weight))
    connection.commit()
    connection.close()
    backmenu()
    

def show_fun(): # show_fun funkcia sluzi na zobrazenie aktualnych zaznamov v databaze sqlite3
    global add_frame
    add_frame = Frame(root)
    add_frame.grid(row=0, column=0, sticky="nsew")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM trening_results")
    records = cursor.fetchall() # Vyberie vsetky zaznamy v databaze trening_results
    connection.close()
    showLabel = Label(add_frame,width=75, height=10,font=("TkHeadingFont",10))
    showLabel.grid(row=2,column=0,padx=20,pady=1)
    TextLabel = Label(add_frame,text="Current data in the database")
    TextLabel.grid(row=1,column=0,padx=20,pady=5)
    print_records = "" # vytvori prazdnu premennu
    for record in records: # for cyklus, ktory vypise data s databazy vo formatovanom stave
        print_records +="ID:" + str(record[0]) + ", DATE: " + str(record[1]) + ", TIME:" + str(record[2]) + ", EXERCISE:" + str(record[3]) + ", REPEAT.:" + str(record[4]) + ", SERIES:" + str(record[5]) + ", WEIGHT:" + str(record[6]) + "\n"

    showLabel.config(text=print_records) # Textovy widget sa upravi na text z premennej print_records
    BackButtonADD = Button(add_frame, text="Home", command=backmenu, width=13, height=2,font=("TkHeadingFont",12), cursor="hand2")
    BackButtonADD.grid(row=4,column=0,padx=20,pady=10)

def compare_fun(): # compare_fun sluzi na porovnanie rovnakych zaznamov nachadzajucich sa v databaze
    global add_frame
    add_frame = Frame(root)
    add_frame.grid(row=0, column=0, sticky="nsew")
    def writecompare():
        exercise = exerciseEntry.get()
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM trening_results WHERE exercise = ? ORDER BY id DESC LIMIT 2", (exercise,)) # Vyberie posledne dve zoznamy z databazy, kde stplec exercise odpoveda zadaneho ID od uzivatela 
        record = cursor.fetchall()
        connection.close()
        resultLabel = Label(add_frame,text="") # Widget textu, ktory bude vypisovat aktualne skore porovnania
        resultLabel.grid()
        if len(record) >= 2: # if podmienka, ktora sa vykona ak su v databaze rovnake aspon dva zoznamy
            previous_record = record[1] # Docasna premenna previous_record v ktorej su ulozene data z druheho zaznamu(starsieho)
            current_record = record[0] # Premenna current_record v ktorej su ulozene data z prveho zaznamu(novsieho)
            previous_weight = previous_record[6] 
            current_weight = current_record[6]
            previous_rep = previous_record[4]
            current_rep = current_record[4]
            previous_ser = previous_record[5]
            current_ser = current_record[5]

            weightupscaling = ((current_weight/previous_weight) -1) * 100 # Vzorec na vypocet weightupscaling: cur_weight/ previos nasledne sa odčita -1 a vynasobi
            repupscaling = ((current_rep/previous_rep)-1) * 100
            serupscaling = ((current_ser/previous_ser)-1) * 100
            upscaling = ((weightupscaling + repupscaling + serupscaling)) / 3
            resultLabel.config(text=f"Increase in performance {exercise} is {upscaling:.2f} %", width=33, height=2,font=("TkHeadingFont",12))
            
        else:
            resultLabel.config(text="At least 2 records must be available for comparison.")

    exercise = Label(add_frame,text="Enter the name of the exercise you want to compare:", width=40, height=2,font=("TkHeadingFont",12)) 
    exercise.grid(row=1,column=0,padx=20,pady=1)
    exerciseEntry = Entry(add_frame)
    exerciseEntry.grid(row=2,column=0,padx=20,pady=1)
    submitadd = Button(add_frame, text="Compare", command=writecompare,width=13, height=1,font=("TkHeadingFont",12), cursor="hand2")
    submitadd.grid(row=3,column=0,padx=20,pady=7)
    BackButtonADD = Button(add_frame, text="Home", command=backmenu,width=13, height=1,font=("TkHeadingFont",12), cursor="hand2")
    BackButtonADD.grid(row=4,column=0,padx=20,pady=7)

def edit_fun(): # edit_fun sluzi na editovanie zoznamu z databazy
    global add_frame
    add_frame = Frame(root, width=500, height=500)
    add_frame.grid(row=0, column=0, sticky="nsew")
    def confirm(new_exercise,new_number_of_repetitions,new_number_of_series,new_weight,id_value):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("UPDATE trening_results SET exercise = ?,"  # Aktualizuje jednotlive polozky a v databaze na zaklade ID
                       "number_of_repetitions = ?,"
                       "number_of_series = ?,"
                       "weight = ? WHERE id = ?", 
                        (new_exercise, new_number_of_repetitions, new_number_of_series, new_weight, id_value))
        connection.commit()
        connection.close()
        backmenu()
    def writenedit2():
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
       # Try except podmienka sluziaca na zistenie ci uzivatel zadal int formu ID
        try:
            id_value = int(idEntry.get()) # Ziska hodnotu ID, ktoru zadal uzivatel na vstupe
        except ValueError:
            idediterror = Label(add_frame, text="Enter id in int format!")
            idediterror.grid()
            return
        
        cursor.execute("SELECT * FROM trening_results WHERE id=?", (id_value,)) # Vyberie vsetky zaznamy kde sa nachadza zadane id_value
        records = cursor.fetchone()  

        if records is None: # if podmienka, ktora zisti ci sa dane ID nachadza v databaze ak nie vrati return a vypise text
            noidedit = Label(add_frame,text="The entered ID is not in the database!")
            noidedit.grid()
            return
        # try except podmienka na overenie spravnej zadanej hodnoty od uzivatela
        try:
             new_number_of_repetitions_val = int(new_number_of_repetitions.get())
        except ValueError:
            idediterror1 = Label(add_frame, text="Enter the number of repetitions in the format int!")
            idediterror1.grid()
            return
        try:
            new_number_of_series_val = int(new_number_of_series.get())
        except ValueError:
            idediterror2 = Label(add_frame, text="Enter the number of series in the format int!")
            idediterror2.grid()
            return
        try:
            new_weight_val = float(new_weight.get())
        except ValueError:
            idediterror3 = Label(add_frame, text="Enter the weight in float or int format!")
            idediterror3.grid()
            return

        new_exercise = new_exerciseEntry.get()
        # Zavolanie funkcie confirm s novymi hodnotami pre databazu
        confirm(new_exercise, new_number_of_repetitions_val, new_number_of_series_val, new_weight_val, id_value)

    idedit = Label(add_frame,text="Enter the id of the exercise on edit:",width=33, height=2,font=("TkHeadingFont",12))
    idedit.grid(row=1,column=0,padx=20,pady=1)
    idEntry = Entry(add_frame)
    idEntry.grid(row=2,column=0,padx=20,pady=1)
    new_exerciseL = Label(add_frame,text="Enter a new exercise name:",width=33, height=2,font=("TkHeadingFont",12))
    new_exerciseL.grid(row=3,column=0,padx=20,pady=1)
    new_exerciseEntry = Entry(add_frame)
    new_exerciseEntry.grid(row=4,column=0,padx=20,pady=1)
    new_number_of_repetitionsL = Label(add_frame,text="Enter the new number of repetitions:",width=33, height=2,font=("TkHeadingFont",12))
    new_number_of_repetitionsL.grid(row=5,column=0,padx=20,pady=1)
    new_number_of_repetitions = Entry(add_frame)
    new_number_of_repetitions.grid(row=6,column=0,padx=20,pady=1)
    new_number_of_seriesL = Label(add_frame,text="Enter the new number of series:",width=33, height=2,font=("TkHeadingFont",12)) 
    new_number_of_seriesL.grid(row=7,column=0,padx=20,pady=1)
    new_number_of_series = Entry(add_frame)
    new_number_of_series.grid(row=8,column=0,padx=20,pady=1)
    new_weightL = Label(add_frame,text="Enter the new number of weight:",width=33, height=2,font=("TkHeadingFont",12)) 
    new_weightL.grid(row=9,column=0,padx=20,pady=1)
    new_weight = Entry(add_frame)
    new_weight.grid(row=10,column=0,padx=20,pady=1)
    submitadd2 = Button(add_frame, text="Confirm", command=writenedit2 ,width=13, height=1,font=("TkHeadingFont",12), cursor="hand2")
    submitadd2.grid(row=11,column=0,padx=20,pady=7)  
    BackButtonADD = Button(add_frame, text="Home", command=backmenu,width=13, height=1,font=("TkHeadingFont",12), cursor="hand2")
    BackButtonADD.grid(row=12,column=0,padx=20,pady=7)

# remove_fun sluzi na odstranenie jedneho, alebo vsetkych zaznamov v databaze   
def remove_fun(): 
    
    global add_frame, removeonlyEntry
    add_frame = Frame(root)
    add_frame.grid(row=0, column=0, sticky="nsew")
    def removefunc(id_value):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM trening_results WHERE id=?",(id_value,)) # Odstrani zaznam kde sa nachadza zadane ID
        connection.commit()
        connection.close()
        removecomplete = Label(add_frame, text="The deletion of the data was successful.")
        removecomplete.grid()
        
    def removeconfig():
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM trening_results")
        result = cursor.fetchone()

        if result is None:
            norecords = Label(add_frame, text="There are no records in the database.")
            norecords.grid()
        else:
            id_value= None
            try:
                id_value = int(removeonlyEntry.get())
            except ValueError:
                idediterror = Label(add_frame, text="Enter the id in the format int!",width=33, height=2,font=("TkHeadingFont",11))
                idediterror.grid()
                return
            except UnboundLocalError as e:
                print(f"{e}")
                return
        
        removefunc(id_value)
    
    def removeconfigall():
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM trening_results")
        result = cursor.fetchone()
        if result is None:
            norecords = Label(add_frame, text="There are no records in the database")
            norecords.grid()
        else:
            cursor.execute("DELETE FROM trening_results") # Odstrani vsetky zaznamy z trening_results
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='trening_results'") # zresetuje pocitadlo ID
            norecords2 = Label(add_frame, text="The deletion of the data from the database was successful.")
            norecords2.grid()
        connection.commit()
        connection.close()
        print("REMOVEconfigall fun")
    def showe():
        removeonly.grid()
        removeonlyEntry.grid()
        showeB = Button(add_frame, text="Confirm", command=removeconfig,width=33, height=2,font=("TkHeadingFont",12))
        showeB.grid(row=10,column=0,padx=20,pady=8)
        
    removeonly = Label(add_frame,text="Enter the value of the int which you want to remove:",width=33, height=2,font=("TkHeadingFont",12))
    removeonlyEntry = Entry(add_frame)
    
    submitremove = Button(add_frame, text="Remove one record from database", command=showe,width=33, height=2,font=("TkHeadingFont",12), cursor="hand2")
    submitremove.grid(row=3,column=0,padx=20,pady=2)
    submitremove2 = Button(add_frame, text="Delete all records from the database", command=removeconfigall,width=33, height=2,font=("TkHeadingFont",12), cursor="hand2")
    submitremove2.grid(row=4,column=0,padx=20,pady=2)
    BackButtonADD = Button(add_frame, text="Home", command=backmenu,width=33, height=2,font=("TkHeadingFont",12), cursor="hand2")
    BackButtonADD.grid(row=5,column=0,padx=20,pady=10)


root.eval("tk::PlaceWindow . center") # Otvori tkinter GUI APP v strede pracovnej obrazovky
frame1 = Frame(root, width=500, height=600, bg="#0EB475") # Vytvori frame(obraz) s rozmermi 500px na sirku a 600 px na vysku a nastavi farbu
frame1.grid(row=0, column=0)
frame1.tkraise() # nastavi prioritu pre frame1 nad ostatnymi widgetami
myLabel1 = Label(frame1, text="Choose the action you want to take:", width=33, height=2,font=("TkHeadingFont",12), bg="#0EB475",) # vytvori text, ktory sa zobrazi na frame1
myLabel1.grid(row=1,column=0,padx=20,pady=15) # umiestnenie objektu
EditButton = Button(frame1, text="Edit data in the database", command=edit_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12)) # vytvori tlacitko 
EditButton.grid(row=2,column=0,padx=18,pady=5)
AddButton = Button(frame1, text="Adding new records to the database", command=add_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12))
AddButton.grid(row=3,column=0,padx=18,pady=5)
CompareButton = Button(frame1, text="Compare your results in the database", command=compare_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12))
CompareButton.grid(row=4,column=0,padx=18,pady=5)
ShowButton = Button(frame1, text="Show entire record from database",command=show_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12))
ShowButton.grid(row=5,column=0,padx=18,pady=5)
RemoveButton = Button(frame1, text="Delete a record from the database", command=remove_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12))
RemoveButton.grid(row=6,column=0,padx=18,pady=5)


root.mainloop()
