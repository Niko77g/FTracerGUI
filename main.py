from tkinter import *
import sqlite3
import datetime
from classOOP import Data


root = Tk()
root.resizable(False, False)
def add_fun():
    global add_frame, exerciseEntry, number_of_repetitionsEntry, number_of_seriesEntry, weightEntry
    add_frame = Frame(root)
    add_frame.grid(row=0,column=0, sticky="nsew")

    exercise = Label(add_frame,text="Zadajte nazov cviku, ktory chcete zapisat:", width=33, height=2,font=("TkHeadingFont",12))
    exercise.grid(row=1,column=0,padx=20,pady=1)
    exerciseEntry = Entry(add_frame)
    exerciseEntry.grid(row=2,column=0,padx=20,pady=1)

    number_of_repetitions = Label(add_frame, text="Zadajte pocet opakovani:", width=33, height=2,font=("TkHeadingFont",12))
    number_of_repetitions.grid(row=3, column=0,padx=20,pady=1)
    number_of_repetitionsEntry = Entry(add_frame)
    number_of_repetitionsEntry.grid(row=4,column=0,padx=20,pady=1)
    number_of_series = Label(add_frame, text="Zadajte pocet serii: ", width=33, height=2,font=("TkHeadingFont",12))
    number_of_series.grid(row=5,column=0,padx=20,pady=1)
    number_of_seriesEntry = Entry(add_frame)
    number_of_seriesEntry.grid(row=6,column=0,padx=20,pady=1)
    weight = Label(add_frame, text="Zadajte vahu v kg:", width=33, height=2,font=("TkHeadingFont",12))
    weight.grid(row=7,column=0,padx=20,pady=1)
    weightEntry = Entry(add_frame)
    weightEntry.grid(row=8,column=0,padx=20,pady=1)
    date = datetime.datetime.now().strftime("%m/%d/%Y")
    time = datetime.datetime.now().strftime("%H:%M")
    new_data = Data(exercise,number_of_repetitions,number_of_series,weight)
    submitadd = Button(add_frame,text="Zapisat",command=writefun,width=13, height=1,font=("TkHeadingFont",12), cursor="hand2")
    submitadd.grid(row=9,column=0,padx=20,pady=7)
    BackButtonADD = Button(add_frame, text="Back to menu", command=backmenu, cursor="hand2",width=13, height=1,font=("TkHeadingFont",12))
    BackButtonADD.grid(row=10,column=0,padx=20,pady=7)

def backmenu():
    add_frame.grid_remove()
    frame1.tkraise()
def writefun():
    date = datetime.datetime.now().strftime("%m/%d/%Y")
    time = datetime.datetime.now().strftime("%H:%M")
    exercise = exerciseEntry.get()
    
    try:
        number_of_repetitions = int(number_of_repetitionsEntry.get())
        number_of_series = int(number_of_seriesEntry.get())
    except ValueError:
        erroradd = Label(add_frame,text="Hodnota pre počet serii a opakovani musi byť cele číslo!")
        erroradd.grid()
        return
    try:
        weight = float(weightEntry.get())
    except ValueError:
        error2add = Label(add_frame,text="Hodnota pre vahu musi byt vo formate float alebo int!")
        error2add.grid()
        return
    print(f"Zapisujem: {exercise,number_of_repetitions,number_of_series,weight}")
    connection = sqlite3.connect("trening_results.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS trening_results(id integer PRIMARY KEY AUTOINCREMENT,date integer,time integer,exercise text,number_of_repetitions integer,number_of_series integer,weight float)")
    cursor.execute("INSERT INTO trening_results(date,time,exercise,number_of_repetitions, number_of_series, weight) VALUES (?,?,?,?,?,?)", (date, time, exercise, number_of_repetitions, number_of_series, weight))
    connection.commit()
    connection.close()
    

def show_fun():
    global add_frame
    add_frame = Frame(root)
    add_frame.grid(row=0, column=0, sticky="nsew")
    connection = sqlite3.connect("trening_results.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM trening_results")
    records = cursor.fetchall()
    connection.close()
    showLabel = Label(add_frame,width=35, height=10,font=("TkHeadingFont",12))
    showLabel.grid(row=2,column=0,padx=20,pady=1)
    TextLabel = Label(add_frame,text="ID, DATUM, CAS, CVIK, POCET OPAKOVANI, POCET SERII, VAHA")
    TextLabel.grid(row=1,column=0,padx=20,pady=5)
    print_records = ""
    for record in records:
        print_records +=", ".join(map(str,record)) + "\n"

    showLabel.config(text=print_records)
    BackButtonADD = Button(add_frame, text="Back to menu", command=backmenu, width=13, height=2,font=("TkHeadingFont",12), cursor="hand2")
    BackButtonADD.grid(row=4,column=0,padx=20,pady=10)

def compare_fun():
    global add_frame
    add_frame = Frame(root)
    add_frame.grid(row=0, column=0, sticky="nsew")
    def writecompare():
        exercise = exerciseEntry.get()
        connection = sqlite3.connect("trening_results.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM trening_results WHERE exercise = ? ORDER BY id DESC LIMIT 2", (exercise,))
        record = cursor.fetchall()
        connection.close()
        resultLabel = Label(add_frame,text="")
        resultLabel.grid()
        if len(record) >= 2:
            previous_record = record[1]
            current_record = record[0]
            previous_weight = previous_record[6]
            current_weight = current_record[6]
            previous_rep = previous_record[4]
            current_rep = current_record[4]
            previous_ser = previous_record[5]
            current_ser = current_record[5]

            weightupscaling = ((current_weight/previous_weight) -1) * 100
            repupscaling = ((current_rep/previous_rep)-1) * 100
            serupscaling = ((current_ser/previous_ser)-1) * 100
            upscaling = ((weightupscaling + repupscaling + serupscaling)) / 3
            resultLabel.config(text=f"Narast vykonu {exercise} je {upscaling:.2f} %", width=33, height=2,font=("TkHeadingFont",12))
            print("Som na konci if podmienke!", upscaling)
        else:
            resultLabel.config(text="Pre porovnanie musia byť k dispozícii aspoň 2 záznamy.")

    exercise = Label(add_frame,text="Zadajte nazov cviku, ktory chcete porovnat:", width=33, height=2,font=("TkHeadingFont",12))
    exercise.grid(row=1,column=0,padx=20,pady=1)
    exerciseEntry = Entry(add_frame)
    exerciseEntry.grid(row=2,column=0,padx=20,pady=1)
    submitadd = Button(add_frame, text="Porovnat", command=writecompare,width=13, height=1,font=("TkHeadingFont",12), cursor="hand2")
    submitadd.grid(row=3,column=0,padx=20,pady=7)
    BackButtonADD = Button(add_frame, text="Back to menu", command=backmenu,width=13, height=1,font=("TkHeadingFont",12), cursor="hand2")
    BackButtonADD.grid(row=4,column=0,padx=20,pady=7)

def edit_fun():
    global add_frame
    add_frame = Frame(root, width=500, height=500)
    add_frame.grid(row=0, column=0, sticky="nsew")
    def confirm(new_exercise,new_number_of_repetitions,new_number_of_series,new_weight,id_value):
        connection = sqlite3.connect("trening_results.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE trening_results SET exercise = ?, number_of_repetitions = ?, number_of_series = ?, weight = ? WHERE id = ?", (new_exercise, new_number_of_repetitions, new_number_of_series, new_weight, id_value))
        connection.commit()
        connection.close()
        backmenu()
    def writenedit2():
        try:
            id_value = int(idEntry.get())
        except ValueError:
            idediterror = Label(add_frame, text="Zadajte id vo formate int!")
            idediterror.grid()
            return
        try:
             new_number_of_repetitions_val = int(new_number_of_repetitions.get())
        except ValueError:
            idediterror1 = Label(add_frame, text="Zadajte pocet opakovani vo formate int!")
            idediterror1.grid()
            return
        try:
            new_number_of_series_val = int(new_number_of_series.get())
        except ValueError:
            idediterror2 = Label(add_frame, text="Zadajte pocet serii vo formate int!")
            idediterror2.grid()
            return
        try:
            new_weight_val = float(new_weight.get())
        except ValueError:
            idediterror3 = Label(add_frame, text="Zadajte vahu vo formate float alebo int!")
            idediterror3.grid()
            return

        new_exercise = new_exerciseEntry.get()
        
        confirm(new_exercise, new_number_of_repetitions_val, new_number_of_series_val, new_weight_val, id_value)
        
    idedit = Label(add_frame,text="Zadajte id cviku na edit:",width=33, height=2,font=("TkHeadingFont",12))
    idedit.grid(row=1,column=0,padx=20,pady=1)
    idEntry = Entry(add_frame)
    idEntry.grid(row=2,column=0,padx=20,pady=1)
    new_exerciseL = Label(add_frame,text="Zadajte novy nazov cviku:",width=33, height=2,font=("TkHeadingFont",12))
    new_exerciseL.grid(row=3,column=0,padx=20,pady=1)
    new_exerciseEntry = Entry(add_frame)
    new_exerciseEntry.grid(row=4,column=0,padx=20,pady=1)
    new_number_of_repetitionsL = Label(add_frame,text="Zadajte novy pocet opakovani:",width=33, height=2,font=("TkHeadingFont",12))
    new_number_of_repetitionsL.grid(row=5,column=0,padx=20,pady=1)
    new_number_of_repetitions = Entry(add_frame)
    new_number_of_repetitions.grid(row=6,column=0,padx=20,pady=1)
    new_number_of_seriesL = Label(add_frame,text="Zadajte novy pocet serii:",width=33, height=2,font=("TkHeadingFont",12)) 
    new_number_of_seriesL.grid(row=7,column=0,padx=20,pady=1)
    new_number_of_series = Entry(add_frame)
    new_number_of_series.grid(row=8,column=0,padx=20,pady=1)
    new_weightL = Label(add_frame,text="Zadajte novu maximalnu vahu:",width=33, height=2,font=("TkHeadingFont",12)) 
    new_weightL.grid(row=9,column=0,padx=20,pady=1)
    new_weight = Entry(add_frame)
    new_weight.grid(row=10,column=0,padx=20,pady=1)
    submitadd2 = Button(add_frame, text="Potvrdit", command=writenedit2 ,width=13, height=1,font=("TkHeadingFont",12), cursor="hand2")
    submitadd2.grid(row=11,column=0,padx=20,pady=7)  
    BackButtonADD = Button(add_frame, text="Back to menu", command=backmenu,width=13, height=1,font=("TkHeadingFont",12), cursor="hand2")
    BackButtonADD.grid(row=12,column=0,padx=20,pady=7)
       
def remove_fun():
    
    global add_frame, removeonlyEntry
    add_frame = Frame(root)
    add_frame.grid(row=0, column=0, sticky="nsew")
    def removefunc(id_value):
        connection = sqlite3.connect("trening_results.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM trening_results WHERE id=?",(id_value,))
        connection.commit()
        connection.close()
        removecomplete = Label(add_frame, text="Odstranenie udajov prebehlo uspesne.")
        removecomplete.grid()
        
    def removeconfig():
        connection = sqlite3.connect("trening_results.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM trening_results")
        result = cursor.fetchone()

        if result is None:
            norecords = Label(add_frame, text="V databaze nie su žiadne zaznamy.")
            norecords.grid()
        else:
            id_value= None
            try:
                id_value = int(removeonlyEntry.get())
            except ValueError:
                idediterror = Label(add_frame, text="Zadajte id vo formate int!",width=33, height=2,font=("TkHeadingFont",11))
                idediterror.grid()
                return
            except UnboundLocalError as e:
                print(f"{e}")
                return
        
        removefunc(id_value)
    
    def removeconfigall():
        connection = sqlite3.connect("trening_results.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM trening_results")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='trening_results'")
        cursor.execute("SELECT * FROM trening_results")
        result = cursor.fetchone()
        if result is None:
            norecords = Label(add_frame, text="V databaze nie su žiadne zaznamy.")
            norecords.grid()
        connection.commit()
        connection.close()
        print("REMOVEconfigall fun")
    def showe():
        removeonly.grid()
        removeonlyEntry.grid()
        showeB = Button(add_frame, text="Potvrdit", command=removeconfig,width=33, height=2,font=("TkHeadingFont",12))
        showeB.grid(row=10,column=0,padx=20,pady=8)
        
    removeonly = Label(add_frame,text="Zadajte id cviku, ktory chcete odstranit:",width=33, height=2,font=("TkHeadingFont",12))
    removeonlyEntry = Entry(add_frame)
    
    submitremove = Button(add_frame, text="Odstranit jeden zoznam", command=showe,width=33, height=2,font=("TkHeadingFont",12), cursor="hand2")
    submitremove.grid(row=3,column=0,padx=20,pady=2)
    submitremove2 = Button(add_frame, text="Odstranit cely zoznam", command=removeconfigall,width=33, height=2,font=("TkHeadingFont",12), cursor="hand2")
    submitremove2.grid(row=4,column=0,padx=20,pady=2)
    BackButtonADD = Button(add_frame, text="Back to menu", command=backmenu,width=33, height=2,font=("TkHeadingFont",12), cursor="hand2")
    BackButtonADD.grid(row=5,column=0,padx=20,pady=10)


root.eval("tk::PlaceWindow . center")
frame1 = Frame(root, width=500, height=600, bg="#0EB475")
frame1.grid(row=0, column=0)
frame1.tkraise()
myLabel1 = Label(frame1, text="Zvolte si akciu, ktorú chcete vykonať:", width=33, height=2,font=("TkHeadingFont",12), bg="#0EB475",)
myLabel1.grid(row=1,column=0,padx=20,pady=15)
EditButton = Button(frame1, text="Edit udajov v databaze", command=edit_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12))
EditButton.grid(row=2,column=0,padx=18,pady=5)
AddButton = Button(frame1, text="Pridanie novych zaznamov do databazy", command=add_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12))
AddButton.grid(row=3,column=0,padx=18,pady=5)
CompareButton = Button(frame1, text="Porovnanie svojich vysledkov v databaze", command=compare_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12))
CompareButton.grid(row=4,column=0,padx=18,pady=5)
ShowButton = Button(frame1, text="Zobrazenie aktualných dát z databazy",command=show_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12))
ShowButton.grid(row=5,column=0,padx=18,pady=5)
RemoveButton = Button(frame1, text="Odstranenie zaznamu z databazy", command=remove_fun, width=33, height=2, cursor="hand2", activeforeground="green", font=("TkHeadingFont",12))
RemoveButton.grid(row=6,column=0,padx=18,pady=5)

root.mainloop()
