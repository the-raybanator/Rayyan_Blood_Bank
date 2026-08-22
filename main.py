from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tk_messagebox

from turtle import RawTurtle, TurtleScreen
import time
import pygame as pg
import sqlite3

import animation
import face_detection

pg.init()


class UserData:
    fg = "maroon"
    bg = "pink" # bg of entire frame
    input_bg = "mistyrose"   # bg of the entry/combobox fields
    font = ("Segoe UI", 15)


    def __init__(self, index, name, widget_type, values=[], state="normal"):
        self.index = index
        self.name = name
        self.widget_type = widget_type
        self.values = values
        self.state = state

        self.data = StringVar() # the actual input of the user
        self.isfilled = False
        self.isnumber = False

        self.create_widgets(details_fr)


    def create_widgets(self, frame):
        # Create the label and widget for each element
        if self.index % 2 == 1:  # this logic is used to alternate data and equally spread them
            row, column = ((self.index+1)//2-1, 0)
        else:
            row, column = (self.index//2-1, 2)
        
        Label(frame, text=self.name, fg=UserData.fg, bg=UserData.bg, font=UserData.font, anchor="w").grid(row=row, column=column, padx=(50,10), pady=15)

        if self.widget_type == "entry":
            self.widget = Entry(frame, textvariable=self.data, fg=UserData.fg, bg=UserData.input_bg, font=UserData.font)
        elif self.widget_type == "dropdown":
            self.widget = ttk.Combobox(frame, width=18, textvariable=self.data, values=self.values, state=self.state, style="TCombobox", font=UserData.font)

        self.widget.grid(row=row, column=column+1)   # add widget to the screen


    def verify_numbers(self, msg="invalid input"):
        if self.isfilled:
            self.isnumber = False
            try:
                int(self.data.get())
                self.isnumber = True    # if the user has inputted a number, it will
            except:
                self.data.set(msg)
                return 1


    def data_warning(self, heading, description):
        result = tk_messagebox.askquestion(f"{heading} Warning", description, icon='warning')
        if result != 'yes':
            exit_func(input_sc)


def disable_event():    # used as formality for the screens
   pass


def add_menu(prev_sc, next_sc, current_sc):  # creates the menu for each screen
    menu_fr = Frame(current_sc, bg="maroon")
    menu_fr.pack(side=BOTTOM, pady=10, anchor=CENTER)

    Button(menu_fr, width=10, text="Previous", fg="black", bg="pink", font=("Segoe UI", 15, "bold"), command=lambda:change_sc(mode = "P", prev_sc = prev_sc, current_sc = current_sc)).grid(padx=5, row=0, column=0, pady=5)
    Button(menu_fr, width=10, text="Next", fg="white", bg="red", font=("Segoe UI", 15, "bold"), command=lambda:change_sc(mode = "N", next_sc = next_sc, current_sc = current_sc)).grid(padx=5, row=0, column=1, pady=5)
    Button(menu_fr, width=10, text="Exit", fg="white", bg="black", font=("Segoe UI", 15, "bold"), command=lambda:change_sc(mode = "E", current_sc = current_sc)).grid(padx=5, row=0, column=2)

    if current_sc == input_sc:    # add clear button just for the input screen
        Button(menu_fr, width=10, text="Clear", fg="black", bg="white", font=("Segoe UI", 15, "bold"), command=clear_data).grid(padx=5, row=0, column=3)


def add_title(sc, index, heading):
    title_fr = Frame(sc)
    title_fr.pack(pady=30)
    Label(title_fr, text=f"Step {index}:", fg="white", bg="maroon", font=('Helvetica', 50, "bold"), borderwidth=2, relief="solid").grid(row=0, column=0)
    Label(title_fr, text=heading, fg="white", bg="maroon", font=('Helvetica', 50, "bold")).grid(row=0, column=1)


def clear_data(warning=True):
    global proceed_to_next
    if warning:
        result = tk_messagebox.askquestion("Clear Data", '''Are you sure you want to clear all the data in this screen?
        (Your data won't be saved...)''', icon='warning')
        if result == 'yes':
            clear_data(warning=False)
    else:
        for i in lst_of_data:
            i.data.set("")  # clears each entry
            i.isfilled = False
            i.isnumber = False
            proceed_to_next = False

def verify_details():
    global proceed_to_next

    error = 0   # innocent until proven guilty

    for i in lst_of_data:
        if i.data.get() in ["", "empty field", "invalid input"]:
            if not(gender.data.get() != "Female" and i == feminine): # to ensure that feminine needs to be filled only when the female gender is selected
                i.isfilled = False
                i.data.set("empty field")
                error = 1
        else:
            i.isfilled = True

    for i in [age, contact, pulse, height, weight]:
        i.verify_numbers()
        if i.verify_numbers() == 1:
            error = 1

    if contact.isnumber:
        if len(contact.data.get()) != 10:
            contact.data.set("Invalid number.")
            error = 1

    if age.isnumber:
        if not(18 <= int(age.data.get()) <= 65):
            age.data_warning("Age", "You are out of the ideal age range, proceed with caution and only if its an emergency.")

    if frequency.data.get() == 'Yes':
        frequency.data_warning("Frequency", "You have donated/received blood too recently, it can be risky. Proceed with caution and only if its an emergency.")

    if restrictions.data.get() != 'None' and restrictions.isfilled:
        restrictions.data_warning("Health", "Your condition might worsen, it can be risky. Proceed with caution and only if its an emergency.")

    if consumptions.data.get() != 'None' and consumptions.isfilled:
        if transaction_type == "Donors":
            tk_messagebox.showwarning("Consumption Warning", "It is too risky to donate, you CANNOT PROCEED. Don't consume it and then come to donate, please.", icon="warning")
            exit_func(input_sc)
        else:
            restrictions.data_warning("Consumption", "BE AWARE THAT THIS CAN BE RISKY. Proceed with caution and only if its an emergency.")
        

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
    else:
        proceed_to_next = False 


def change_sc(mode, current_sc, prev_sc = 0, next_sc = 0):
    global proceed_to_next
    if prev_sc == sc:
        return

    if not(next_sc == process and not face_detection.proceed_to_next): # to ensure that next btn is disabled if user hasnt captured yet
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
        if (face_detection.proceed_to_next and current_sc == img_capt) or current_sc in [process, confirm]:   # to bypass the webcam stage and process, and confirmation
            proceed_to_next = True

        if proceed_to_next:
            proceed_to_next = False

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


def insertBLOB():
    conn = sqlite3.connect('User Profiles/Database.db')

    empPhoto = convertToBinaryData("User Profiles/{}/ID_[{}].png".format(transaction_type, current_id))

    data_to_store = [i.data.get() for i in lst_of_data]
    data_to_store.append(empPhoto)

    conn.execute(f'''INSERT INTO {transaction_type} (
    "NAME",
    "AGE",
    "GENDER",
    "LAST VISITED",
    "BLOOD GROUP",
    "CONTACT NUMBER",
    "EMAIL ID",
    "HOME ADDRESS",
    "PULSE RATE",
    "HEIGHT",
    "WEIGHT",
    "RESTRICTIONS",
    "CONSUMPTIONS",
    "FEMININE",
    "PHOTO")
    
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
    data_to_store)
    
    conn.commit()
    conn.close()

def progressbar():
    p.config(mode='determinate')
    p['value'] = 0
    for i in range(5):
        p['value'] += 20
        the_end.update_idletasks()
        time.sleep(0.5)
    
    saved = Label(the_end, text='Saved Successfully', fg='lime', bg="maroon", font=("Segoe UI", 25, "bold"))
    saved.pack()
    the_end.update()
    time.sleep(1)
    the_end.withdraw()
    saved.forget()

    insertBLOB()
    exit_func(the_end, show_warning=False)


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

    details_fr.grid_columnconfigure(0, weight=1)        # used to ensure that the columns are equally wide and split across screen
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

    save_data_frame = Frame(input_sc, bg="maroon")
    save_data_frame.pack(pady=(15,0))
    Label(save_data_frame, text="Click to save, once data is verified you can proceed", fg="mistyrose", bg="maroon", font=("Segoe UI", 15, "bold")).grid(row=0, column=0)
    Button(save_data_frame, text="Save Data", bg="lightgreen", height=1, font=("Segoe UI", 15, "bold"), command=verify_details).grid(row=0, column=1, padx=(15,0))

    # STEP 2: FACE CAPTURE
    img_capt.title('{} - Note for Capturing Face'.format(transaction_type))
    add_title(img_capt, 2, "Capture Your Image")
    add_menu(prev_sc=input_sc, current_sc=img_capt, next_sc=process)

    Label(img_capt, fg="mistyrose", bg="maroon", font=("Segoe UI", 15), text="Your webcam will be on and you are requested to take a clear picture of yourself.").pack(pady=10)
    
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

    # Create an identical frame to display user data for verifying
    confirm_fr = Listbox(confirm, bg='pink')
    confirm_fr.pack(pady=(10, 0), fill=X, padx=15)

    confirm_fr.grid_columnconfigure(0, weight=1)        # used to ensure that the columns are equally wide and split across screen
    confirm_fr.grid_columnconfigure(1, weight=1)
    confirm_fr.grid_columnconfigure(2, weight=1)
    confirm_fr.grid_columnconfigure(3, weight=1)

    Label(confirm, fg="mistyrose", bg="maroon", font=("Segoe UI", 15), text="BE CAREFUL! Once you confirm, there is NO GOING BACK!!").pack()
    
    for i in lst_of_data:
        i.create_widgets(confirm_fr)

    # STEP 5: SAVE DATA & CONCLUDE
    the_end.title('{} - Thank You for Choosing Us!'.format(transaction_type))

    Label(the_end, text='''Now you are done. Thank you for choosing us!
    We hope you come next time; Till then, bye!''',
          font=('bold', 25), fg='blue', bg='light blue').pack()
    Save_All_Data=Button(the_end, text='Save All Data', command=progressbar, bg='lime', font=('bold', 20))
    Save_All_Data.pack(pady=(20, 0))
    p=ttk.Progressbar(the_end, orient=HORIZONTAL, length=500, mode='indeterminate')
    p.pack(pady=20)


def exit_func(current_sc, destroy=False, show_warning=True):
    if destroy:
        sc.withdraw()
        animation.draw(turtle_sc, screen_length, screen_width)
        root.destroy()

    else:
        result = tk_messagebox.askquestion("Exit", "Are you sure you exit? (Your data won't be saved...)",
                                               icon='warning')
        if result == 'yes':
            clear_data(warning=False)
            face_detection.proceed_to_next = False

            for i in [input_sc, img_capt, process, confirm, the_end]:
                for widget in i.winfo_children():
                    widget.destroy()
            
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
