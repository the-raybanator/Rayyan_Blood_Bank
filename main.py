from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tk_messagebox

from turtle import RawTurtle, TurtleScreen
import time
import datetime
import pygame as pg
import sqlite3

import animation
import face_detection

pg.init()


class UserData:
    fg = "maroon"
    bg = "pink" # bg of entire frame
    input_bg = "mistyrose"   # bg of the entry/combobox fields
    font=("Segoe UI", 15)

    def __init__(self, index, name, widget_type, values=[], state="normal"):
        self.index = index
        self.widget_type = widget_type
        self.data = StringVar() # the actual input of the user
        self.isfilled = False

        # Create the label and widget for each element
        if index % 2 == 1:  # this logic is used to alternate data and equally spread them
            row, column = ((index+1)//2-1, 0)
        else:
            row, column = (index//2-1, 2)
        
        Label(details_fr, text=name, fg=UserData.fg, bg=UserData.bg, font=UserData.font, anchor="w").grid(row=row, column=column, padx=(50,10), pady=15)

        if self.widget_type == "entry":
            self.widget = Entry(details_fr, textvariable=self.data, fg=UserData.fg, bg=UserData.input_bg, font=UserData.font)
        elif self.widget_type == "dropdown":
            self.widget = ttk.Combobox(details_fr, width=18, textvariable=self.data, values=values, state=state, style="TCombobox", font=UserData.font)

        self.widget.grid(row=row, column=column+1)   # add widget to the screen




def disable_event():    # used as formality for the screens
   pass


def add_menu(prev_sc, next_sc, current_sc):  # creates the menu for each screen
    menu_fr = Frame(current_sc, bg="maroon")
    menu_fr.pack(side=BOTTOM, pady=10, anchor=CENTER)

    Button(menu_fr, width=10, text="Previous", fg="black", bg="pink", font=("Segoe UI", 15, "bold"), command=lambda:change_sc(mode = "P", prev_sc = prev_sc, current_sc = current_sc)).grid(padx=5, row=0, column=0, pady=5)
    Button(menu_fr, width=10, text="Next", fg="white", bg="red", font=("Segoe UI", 15, "bold"), command=lambda:change_sc(mode = "N", next_sc = next_sc, current_sc = current_sc)).grid(padx=5, row=0, column=1, pady=5)
    Button(menu_fr, width=10, text="Exit", fg="white", bg="black", font=("Segoe UI", 15, "bold"), command=lambda:change_sc(mode = "E", current_sc = current_sc)).grid(padx=5, row=0, column=2)

    if current_sc == input_sc:    # add clear button just for the input screen
        Button(menu_fr, width=10, text="Clear", fg="black", bg="white", font=("Segoe UI", 15, "bold"), command=clear_sc).grid(padx=5, row=0, column=3)


def add_title(sc, index, heading):
    title_fr = Frame(sc)
    title_fr.pack(pady=30)
    Label(title_fr, text=f"Step {index}:", fg="white", bg="maroon", font=('Helvetica', 50, "bold"), borderwidth=2, relief="solid").grid(row=0, column=0)
    Label(title_fr, text=heading, fg="white", bg="maroon", font=('Helvetica', 50, "bold")).grid(row=0, column=1)


def clear_sc(warning=True):
    if warning:
        result = tk_messagebox.askquestion("Clear Data", '''Are you sure you want to clear all the data in this screen?
        (Your data won't be saved...)''', icon='warning')
        if result == 'yes':
            clear_sc(warning=False)
    else:
        for i in lst_of_data:
            i.data.set("")  # clears each entry

def verify_details():
    global proceed_to_next

    error = 0   # innocent until proven guilty

    for i in lst_of_data:
        if i.data.get() == "" or i.data.get() == "Empty field!":
            i.isfilled = False
            i.data.set("Empty field!")
            error = 1
        else:
            i.isfilled = True

    if gender.data.get() != "Female":
        feminine.data.set("")

    if age.isfilled:
        try:
            if not(18 <= int(age.data.get()) <= 65):
                result = tk_messagebox.askquestion("Age Warning", "You are out of the ideal age range, proceed with caution and only if its an emergency.", icon='warning')
                if result != 'yes':
                    exit_func(input_sc)

        except:
            age.data.set('Enter age in numbers')
            error = 1

    if frequency.data.get() == 'Yes':
        result = tk_messagebox.askquestion("Frequency Warning", "You have donated/received blood too recently, it can be risky. Proceed with caution and only if its an emergency.", icon='warning')
        if result != 'yes':
            exit_func(input_sc)

    if contact.isfilled:
        try:
            int(contact.data.get())   # to make sure it is an number
            if len(contact.data.get()) != 10:
                contact.data.set("Invalid number.")
                error = 1

        except:
            contact.data.set("Invalid number.")
            error = 1

    if restrictions.data.get() != 'None' and restrictions.isfilled:
        result = tk_messagebox.askquestion("Health Warning", "Your condition might worsen, it can be risky. Proceed with caution and only if its an emergency.", icon='warning')
        if result != 'yes':
            exit_func(input_sc)

    if consumptions.data.get() != 'None' and consumptions.isfilled:
        if transaction_type == "Donors":
            tk_messagebox.showwarning("Consumption Warning", "It is too risky to donate, you CANNOT PROCEED. Don't consume it and then come to donate, please.", icon="warning")
            exit_func(input_sc)
        else:
            result = tk_messagebox.askquestion("Consumption Warning", "BE AWARE THAT THIS CAN BE RISKY. Proceed with caution and only if its an emergency.", icon='warning')
            if result != 'yes':
                exit_func(input_sc)
        

    if feminine.data.get() != 'None' and feminine.isfilled and feminine.data.get() != "":   # feminine.data.get() != "" ensures that it will ignore for when its not relevant
        if transaction_type == "Donors":
            tk_messagebox.showwarning("Feminine Warning", "It is too risky to donate, you CANNOT PROCEED. Come back later.", icon="warning")
            exit_func(input_sc)
        else:
            result = tk_messagebox.askquestion("Feminine Warning", "BE AWARE THAT THIS CAN BE RISKY. Proceed with caution and only if its an emergency.", icon='warning')
            if result != 'yes':
                exit_func(input_sc)

    if error == 0:
        proceed_to_next = True

def show_data():
    confirm_fr = Frame(confirm)
    confirm_fr.pack()
    Label(confirm, text='Below are all the details you mentioned. Kindly check if they are correct as we shall record them!', font=25).pack(pady=10)

    Label(confirm_fr, text='Name', fg='blue', font=20).grid(row=0, column=0)
    Name_c=Entry(confirm_fr, font=20)
    Name_c.delete(0, 'end')
    Name_c.insert(0, Name_input.get())
    Name_c.grid(padx=(15, 0), pady=10, row=0, column=1)

    Label(confirm_fr, height=1, text='Age', fg='blue', font=20).grid(row=1, column=0)
    Age_c = Entry(confirm_fr, font=20)
    Age_c.delete(0, 'end')
    Age_c.insert(0, Age_input.get())
    Age_c.grid(padx=(15, 0), pady=10, row=1, column=1)

    Label(confirm_fr, height=1, text='Gender', fg='blue', font=20).grid(row=2, column=0)
    Gender_c = Entry(confirm_fr, font=20)
    Gender_c.delete(0, 'end')
    Gender_c.insert(0, Gender_o.get())
    Gender_c.grid(padx=(15, 0), pady=10, row=2, column=1)

    Label(confirm_fr, height=1, text='Are you:', fg='blue', font=20).grid(row=2, column=2)
    Female_c = Entry(confirm_fr, font=20)
    Female_c.delete(0, 'end')
    Female_c.insert(0, Female_o.get())
    Female_c.grid(padx=(15, 0), pady=10, row=2, column=3)

    Label(confirm_fr, height=1, text='''   Did you donate
    blood during the
    last six months''', fg='blue', font=20).grid(row=3, column=0)
    Frequency_c = Entry(confirm_fr, font=20)
    Frequency_c.delete(0, 'end')
    Frequency_c.insert(0, Frequency_o.get())
    Frequency_c.grid(padx=(15, 0), pady=10, row=3, column=1)

    Label(confirm_fr, height=1, text='Blood Group:', fg='blue', font=20).grid(row=4, column=0)
    Blood_group_c = Entry(confirm_fr, font=20)
    Blood_group_c.delete(0, 'end')
    Blood_group_c.insert(0, Blood_group_o.get())
    Blood_group_c.grid(padx=(15, 0), pady=10, row=4, column=1)

    Label(confirm_fr, height=1, text='Contact Number', fg='blue', font=20).grid(row=5, column=0)
    Contact_Number_c = Entry(confirm_fr, font=20)
    Contact_Number_c.delete(0, 'end')
    Contact_Number_c.insert(0, Contact_Number_input.get())
    Contact_Number_c.grid(padx=(15, 0), pady=10, row=5, column=1)

    Label(confirm_fr, height=1, text='Email Address', fg='blue', font=20).grid(row=6, column=0)
    Email_id_c = Entry(confirm_fr, font=20)
    Email_id_c.delete(0, 'end')
    Email_id_c.insert(0, Email_id_input.get())
    Email_id_c.grid(padx=(15, 0), pady=10, row=6, column=1)

    Label(confirm_fr, height=1, text='Home Address', fg='blue', font=20).grid(row=7, column=0)
    Address_c = Entry(confirm_fr, font=20)
    Address_c.delete(0, 'end')
    Address_c.insert(0, Address_input.get())
    Address_c.grid(padx=(15, 0), pady=10, row=7, column=1)

    Label(confirm_fr, height=1, text='Contact Number', fg='blue', font=20).grid(row=8, column=0)
    Pulse_rate_c = Entry(confirm_fr, font=20)
    Pulse_rate_c.delete(0, 'end')
    Pulse_rate_c.insert(0, Pulse_rate_input.get())
    Pulse_rate_c.grid(padx=(15, 0), pady=10, row=8, column=1)

    Label(confirm_fr, height=1, text='Height (in cm)', fg='blue', font=20).grid(row=9, column=0)
    Height_c = Entry(confirm_fr, font=20)
    Height_c.delete(0, 'end')
    Height_c.insert(0, Height_input.get())
    Height_c.grid(padx=(15, 0), pady=10, row=9, column=1)

    Label(confirm_fr, height=1, text='Weight (in kg)', fg='blue', font=20).grid(row=10, column=0)
    Weight_c = Entry(confirm_fr, font=20)
    Weight_c.delete(0, 'end')
    Weight_c.insert(0, Weight_input.get())
    Weight_c.grid(padx=(15, 0), pady=10, row=10, column=1)

    Label(confirm_fr, height=1, text='Are you facing', fg='blue', font=20).grid(row=11, column=0)
    Restrictions_c = Entry(confirm_fr, font=20)
    Restrictions_c.delete(0, 'end')
    Restrictions_c.insert(0, Restrictions_o.get())
    Restrictions_c.grid(padx=(15, 0), pady=10, row=11, column=1)

    Label(confirm_fr, height=1, text='Today, have you consumed', fg='blue', font=20).grid(row=12, column=0)
    Consumptions_c = Entry(confirm_fr, font=20)
    Consumptions_c.delete(0, 'end')
    Consumptions_c.insert(0, Consumptions_o.get())
    Consumptions_c.grid(padx=(15, 0), pady=10, row=12, column=1)


def change_sc(mode, current_sc, prev_sc = 0, next_sc = 0):
    if prev_sc == sc:
        return

    try:        # we use try except to ensure code continues even if camera was closed
        face_detection.stop_camera()
    except:
         pass

    pg.mixer.music.load('Assets/Peaceful_Music.wav')
    pg.mixer.music.stop()
    
    if mode == "E":
        exit_func(current_sc)
        return
    
    if mode == "P":
        current_sc.withdraw()
        prev_sc.deiconify()
        if prev_sc == process:
            pg.mixer.music.load('Assets/Peaceful_Music.wav')
            pg.mixer.music.play(-1)
    elif mode=="N":
        if proceed_to_next:
            current_sc.withdraw()
            next_sc.deiconify()
            if next_sc == process:
                pg.mixer.music.load('Assets/Peaceful_Music.wav')
                pg.mixer.music.play(-1)
            elif next_sc==the_end:
                p['value']=0
                p.config(mode='indeterminate')
                the_end.update_idletasks()
                p.start(10) 


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insertBLOB(id):
    conn = sqlite3.connect('User Profiles/Database.db')
    cursor = conn.cursor()

    empPhoto = convertToBinaryData("User Profiles/{}/ID_[{}].png".format(transaction_type, current_id))
    lst=[current_id, Name_c.get(), Age_c.get(), Gender_c.get(), Female_c.get(), Frequency_c.get(), Blood_group_c.get(),
     Contact_Number_c.get(), Email_id_c.get(), Pulse_rate_c,
     Height_c, Weight_c, Restrictions_c, Consumptions_c, empPhoto]

    conn.execute('''INSERT INTO Donors(UNIQUE_ID, NAME, AGE, GENDER, FEMALE_CONDITIONS, LAST, BLOOD_GROUP, CONTACT_NUMBER, EMAIL_ID, PULSE_RATE, 
            HEIGHT_(IN_CM), WEIGHT_(IN_KG), RESTRICTION(S), CONSUMPTION(S), PHOTOGRAPH)\
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (current_id, Name_c.get(), Age_c.get(), Gender_c.get(), Female_c.get(), Frequency_c.get(), Blood_group_c.get(),
     Contact_Number_c.get(), Email_id_c.get(), Pulse_rate_c,
     Height_c, Weight_c, Restrictions_c, Consumptions_c, empPhoto))
    conn.commit()

    cursor.close()
    conn.close()
    print("Image and file inserted successfully as a BLOB into a table")

def progressbar():
    p.config(mode='determinate')
    p['value'] = 0
    for i in range(5):
        p['value'] += 20
        the_end.update_idletasks()
        time.sleep(0.5)
    saved=Label(the_end, text='Saved Successfully', fg='green', font=('bold', 20))
    saved.pack()
    the_end.update()
    time.sleep(1)
    the_end.withdraw()
    saved.forget()

    insertBLOB(current_id)
    exit_func(the_end)


def main(type):
    global transaction_type, current_id, lst_of_data, details_fr, p, proceed_to_next
    global name, age, gender, frequency, blood_group, contact, email_id, address, pulse, height, weight, restrictions, consumptions, feminine

    transaction_type = type

    conn = sqlite3.connect('User Profiles/Database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {}".format(transaction_type))
    current_id = len(cursor.fetchall()) + 1
    cursor.close()
    conn.close()

    sc.withdraw()
    input_sc.deiconify()
    proceed_to_next = False

    # STEP 1: ENTER GENERAL DATA
    input_sc.title("{} - Let's Start".format(transaction_type))
    add_title(input_sc, 1, "Fill In Your Details")
    add_menu(prev_sc=sc, current_sc=input_sc, next_sc=img_capt)

    details_fr = Listbox(input_sc, bg='pink')
    details_fr.pack(pady=(10, 0), fill=X, padx=15)
    details_fr.grid_columnconfigure(0, weight=1)
    details_fr.grid_columnconfigure(1, weight=1)
    details_fr.grid_columnconfigure(2, weight=1)
    details_fr.grid_columnconfigure(3, weight=1)

    name = UserData(1, "Name", "entry")
    age = UserData(2, "Age", "entry")
    gender = UserData(3, "Gender", "dropdown", ['Male', 'Female', "Other (Type It)"])
    frequency = UserData(4, ''' Did you donate
    blood during the
  last six months: ''', "dropdown", ["Yes", "No"], "readonly")
    blood_group = UserData(5, "Blood Group", "dropdown", ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'], "readonly")
    contact = UserData(6, "Contact Number", "entry")
    email_id = UserData(7, "Email Address", "entry")
    address = UserData(8, "Home Address", "entry")
    pulse = UserData(9, "Pulse Rate", "entry")
    height = UserData(10, "Height (in cm)", "entry")
    weight = UserData(11, "Weight (in kg)", "entry")
    restrictions = UserData(12, "Are you facing", "dropdown", ['None', 'Cold', 'Flu', 'Sore Throat', 'Cold Sore', 'Stomach Bug', 'Other (Type It)'])
    consumptions = UserData(13, "Have you consumed", "dropdown", ['None', 'Alcohol', 'Fatty foods', 'Aspirin', 'Iron Blockers', 'Other (Type It)'])
    feminine = UserData(14, '''FOR FEMALES
Are you?''', "dropdown", ['None', 'Pregnant', 'Breastfreeding', "Other (Type It)"])

    lst_of_data = [name, age, gender, frequency, blood_group, contact, email_id, address, pulse, height, weight, restrictions, consumptions, feminine]

    Button(input_sc, text="Save Data", bg="lime", font=("Segoe UI", 15, "bold"), command=verify_details).pack()

    # STEP 2: FACE CAPTURE
    img_capt.title('{} - Note for Capturing Face'.format(transaction_type))
    add_title(img_capt, 2, "Capture Your Image")
    add_menu(prev_sc=input_sc, current_sc=img_capt, next_sc=process)

    Label(img_capt, fg="mistyrose", bg="maroon", font=("Segoe UI", 15), text='''Your webcam will be on and you are requested to take a clear picture of yourself.
                Your whole face should show fully. Try not to cover your face with sunglasses, cap, earmuffs, helmet etc.
                Make sure to save your picture!''').pack(pady=20)
    
    face_detection.create_widgets(img_capt, transaction_type, current_id)

    # STEP 3: THE PROCESS
    process.title("{} - All the Best!!!".format(transaction_type))

    add_title(process, 3, "The Main Process")

    Label(process, fg="mistyrose", bg="maroon", font=("Segoe UI", 15), text='''Now we shall collect your blood. If it is your first time then stay calm! We shall do very carefully. ALL THE BEST!!!''').pack(pady=20)

    pic=Canvas(master=process, width = 200, height = 200)
    pic.pack()
    pic_screen = TurtleScreen(pic)
    pic_screen.register_shape('Assets/good_luck.gif')
    draw = RawTurtle(pic_screen)
    draw.shape('Assets/good_luck.gif')
    draw.goto(0, 0)

    add_menu(prev_sc=img_capt, current_sc=process, next_sc=confirm)

    # STEP 4: DOUBLE CHECK DATA BEFORE SENDING
    confirm.title('{} - One Last Step to go'.format(transaction_type))
    add_title(confirm, 4, "Confirm Your Details")
    add_menu(prev_sc=process, current_sc=confirm, next_sc=the_end)

    Label(confirm, fg="mistyrose", bg="maroon", font=("Segoe UI", 15), text="BE CAREFUL! Once you confirm, there is NO GOING BACK!!").pack()

    # STEP 5: SAVE DATA & CONCLUDE
    the_end.title('{} - Thank You for Choosing Us!'.format(transaction_type))

    Label(the_end, text='''Now you are done. Thank you for choosing us!
    We hope you come next time; Till then, bye!''',
          font=('bold', 25), fg='blue', bg='light blue').pack()
    Save_All_Data=Button(the_end, text='Save All Data', command=progressbar, bg='lime', font=('bold', 20))
    Save_All_Data.pack(pady=(20, 0))
    p=ttk.Progressbar(the_end, orient=HORIZONTAL, length=500, mode='indeterminate')
    p.pack(pady=20)


def exit_func(current_sc, destroy=False):
    if destroy:
        result = tk_messagebox.askquestion("Exit", "Are you sure you want to quit program?",
                                       icon='warning')
        if result == 'yes':
            sc.withdraw()
            animation.draw(turtle_sc, screen_length, screen_width)
            root.destroy()

    else:
        result = tk_messagebox.askquestion("Exit", "Are you sure you exit? (Your data won't be saved...)",
                                               icon='warning')
        if result == 'yes':
            clear_sc(warning=False)
            current_sc.withdraw()
            sc.deiconify()



root = Tk()
root.withdraw()

screen_length = 1500
screen_width = 850

turtle_sc = Toplevel(root)
sc = Toplevel(root)
input_sc = Toplevel(root)
img_capt = Toplevel(root)
process = Toplevel(root)
confirm = Toplevel(root)
the_end = Toplevel(root)


# style for the dropdown menus
input_sc.option_add('*TCombobox*Listbox.font', UserData.font)       # these lines ensure that the entire dropdown menu is styled
input_sc.option_add('*TCombobox*Listbox.background', UserData.input_bg)
input_sc.option_add('*TCombobox*Listbox.foreground', UserData.fg)
input_sc.option_add('*TCombobox*Listbox.selectBackground', UserData.fg)
input_sc.option_add('*TCombobox*Listbox.selectForeground', UserData.input_bg)

style = ttk.Style()
style.theme_use("clam")

style.configure("TCombobox",
borderwidth=0,
relief="flat",
fieldbackground=UserData.input_bg,
background=UserData.input_bg,
foreground=UserData.fg,
selectbackground=UserData.input_bg,
selectforeground=UserData.fg,
font=UserData.font)

style.map("TCombobox",
    fieldbackground=[('readonly', UserData.input_bg)],
    background=[('readonly', UserData.input_bg)],
    foreground=[('readonly', UserData.fg)],
    selectbackground=[('readonly', UserData.input_bg)],
    selectforeground=[('readonly', UserData.fg)])

screens = [turtle_sc, sc, input_sc, img_capt, process, confirm, the_end]

for i in screens:
    i.withdraw()
    i.config(bg="maroon")
    i.geometry(f"{screen_length}x{screen_width}+0+0")
    i.resizable(False, False)
    i.protocol("WM_DELETE_WINDOW", disable_event)

Label(sc, text="What would you like to do?", fg="white", bg="maroon", font=('Courier', 50)).place(anchor=CENTER, relx=.5, rely=.1)
sc_fr = Frame(sc, bg="maroon")
sc_fr.place(anchor=CENTER, relx=.5, rely=.5)
donate = Button(sc_fr, text="DONATE", fg="lime", bg='dark blue', width=30, height= 6, font=("Helvetica", 20, "bold"), command=lambda:main('Donors'))
donate.grid(row=0, column=0, padx=(20, 10))
receive = Button(sc_fr, text="RECEIVE", fg="pink", bg='red', width=30, height= 6, font=("Helvetica", 20, "bold"), command=lambda:main('Receivers'))
receive.grid(row=0, column=2, padx=(10, 20))
Exit = Button(sc_fr, text="EXIT", fg="white", bg='black', width=25, height= 6, font=("Helvetica", 20, "bold"), command=lambda:exit_func(sc, destroy=True))
Exit.grid(row=0, column=1, padx=10)

animation.draw(turtle_sc, screen_length, screen_width)    # starts animation

sc.deiconify()      # once animation is done, the selection screen shows and from there on, code continues

root.mainloop()
