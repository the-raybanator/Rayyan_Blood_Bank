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


def disable_event():    # used as formality for the screens
   pass


def add_menu(prev_sc, next_sc, current_sc):  # creates the menu for each screen
    menu_fr = Frame(current_sc)
    menu_fr.pack(side=BOTTOM, pady=10, anchor=CENTER)

    Button(menu_fr, width=10, text="Previous", fg="black", bg="pink", font=("Segoe UI", 15, "bold"), command=lambda:change_sc(mode = "P", prev_sc = prev_sc, current_sc = current_sc)).grid(padx=5, row=0, column=0, pady=5)
    Button(menu_fr, width=10, text="Next", fg="white", bg="red", font=("Segoe UI", 15, "bold"), command=lambda:change_sc(mode = "N", next_sc = next_sc, current_sc = current_sc)).grid(padx=5, row=0, column=1, pady=5)
    Button(menu_fr, width=10, text="Exit", fg="white", bg="black", font=("Segoe UI", 15, "bold"), command=lambda:change_sc(mode = "E", current_sc = current_sc)).grid(padx=5, row=0, column=2)

    if current_sc == input_sc:    # add clear button just for the input screen
        Button(menu_fr, width=10, text="Clear", fg="black", bg="white", font=("Segoe UI", 15, "bold"), command=clear_sc).grid(padx=5, row=0, column=3)

def clear_sc(warning=True):
    if warning:
        result = tk_messagebox.askquestion("Clear Data", '''Are you sure you want to clear all the data in this screen?
        (Your data won't be saved...)''', icon='warning')
        if result == 'yes':
            clear_sc(warning=False)
    else:
        Name_input.delete(0, len(Name_input.get()))
        Age_input.delete(0, len(Age_input.get()))
        Gender_o.set('')
        Female_o.set('')
        Frequency_o.set('')
        Blood_group_o.set('')
        Contact_Number_input.delete(0, len(Contact_Number_input.get()))
        Email_id_input.delete(0, len(Email_id_input.get()))
        Address_input.delete(0, len(Address_input.get()))
        Pulse_rate_input.delete(0, len(Pulse_rate_input.get()))
        Height_input.delete(0, len(Height_input.get()))
        Weight_input.delete(0, len(Weight_input.get()))
        Restrictions_o.set('')
        Consumptions_o.set('')

def verify_details():
    try:
        if int(Age_input.get())>65:
            input_sc.withdraw()
            tk_messagebox.showinfo("Information", "Sorry... You cannot donate blood as you are above 65 years of age. ")
            error = 1
            return
        elif int(Age_input.get()) < 18:
            today = datetime.date.today()
            age=Label(details_fr, text='You are young to donate! Come on {}'.format((18 - int(Age_input.get())) + int(today.year)), fg='red')
            age.grid(row=1, column=2)
        #elif  bool(age.winfo_ismapped())==True:
         #   age.grid_forget()

    except:
        age=Label(details_fr, text='Enter a valid age which is a number (in years)', fg='red')
        age.grid(row=1, column=2)
        error = 1
    if Frequency_o.get()=='Yes':
        frequency=Label(details_fr, fg='red', text='Sorry... You can donate blood once it has been more than 6 months since you last donated blood')
        frequency.grid(row=2, column=2)
    try:
        x=int(Contact_Number_input.get())
        while x != 0:
            x //= 10
            count += 1
        if count != 10:
            mobile_no=Label(details_fr, fg='red', text='Kindly Recheck your Mobile Number')
            mobile_no.grid(row=3, column=2)
            error = 1

    except:
        mobile_no=Label(details_fr, fg='red', text='Kindly Recheck your Mobile Number')
        mobile_no.grid(row=3, column=2)
        error = 1

    if Restrictions_o.get()=='':
        restrictions=Label(details_fr, fg='red', text='Please select if you are facing the following')
        restrictions.grid(row=11, column=2)
        error = 1
    elif Restrictions_o.get()!='(None)' and Restrictions_o.get()!='':
        restrictions=Label(details_fr, fg='red', text='Get well then come to donate!')
        restrictions.grid(row=11, column=2)

    if Consumptions_o.get()!='':
        consumptions=Label(details_fr, fg='red', text="Please select if you consumed the following")
        consumptions.grid(row=12, column=2)
        error = 1
    elif Consumptions_o.get()!='(None)' and Consumptions_o.get()!='':
        consumptions=Label(details_fr, fg='red', text="Don't consume these then come to donate!")
        consumptions.grid(row=12, column=2)

    if Female_o.get()=='Breastfeeding':
        female=Label(details_fr, fg='red', text='Congratulations! But please come when you are not breastfeeding!')
        female.grid(row=3, column=3)

    elif Female_o.get()=='Pregnant':
        female=Label(details_fr, fg='red', text='Congratulations! But please come when you are not pregnant!')
        female.grid(row=3, column=3)

    elif Female_o.get()!='None of the above' and Gender_o.get()=='Female':
        female=Label(details_fr, fg='red', text='Kindly choose and appropriate option')
        female.grid(row=3, column=3)
        error = 1
    if Name_input.get()=='':
        name=Label(details_fr, fg='red', text='Kindly input your name')
        name.grid(row=0, column=2)
        error = 1
    if Gender_o.get()=='':
        gender=Label(details_fr, fg='red', text='Kindly input your gender')
        gender.grid(row=1, column=2)
        error = 1
    if Frequency_o.get()=='':
        frequency=Label(details_fr, fg='red', text='Kindly input whether you donated blood within the last 6 months.')
        frequency.grid(row=2, column=2)
        error = 1
    if Email_id_input.get()=='':
        email_id=Label(details_fr, fg='red', text='Kindly input your email address')
        email_id.grid(row=3, column=2)
        error = 1
    if Address_input.get()=='':
        address=Label(details_fr, fg='red', text='Kindly input your home address')
        address.grid(row=4, column=2)
        error = 1
    if Pulse_rate_input.get()=='':
        pulse_rate=Label(details_fr, fg='red', text='Kindly input your pulse rate')
        pulse_rate.grid(row=5, column=2)
        error = 1
    if Height_input.get()=='':
        height=Label(details_fr, fg='red', text='Kindly input your height')
        height.grid(row=6, column=2)
        error = 1
    if Weight_input.get()=='':
        weight=Label(details_fr, fg='red', text='Kindly input your weight')
        weight.grid(row=7, column=2)
        error=1
    if error == 0:
        change_sc(0, img_capt, input_sc, 'N')

def show_data():
    global Name_c, Age_c, Gender_c, Female_c, Frequency_c, Blood_group_c, Contact_Number_c, Email_id_c, Pulse_rate_c,\
        Height_c, Weight_c, Restrictions_c, Consumptions_c

    Step4_fr = Frame(confirm)
    Step4_fr.pack()
    Label(Step4_fr, text="Step 4:", font=('Courier', 30), borderwidth=2, relief="solid").grid(row=0, column=0)
    Label(Step4_fr, text='Confirm Your Details', font=('Courier', 30)).grid(row=0, column=1)

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

    #confirm.update()
def change_sc(mode, current_sc, prev_sc = 0, next_sc = 0):
    if prev_sc == sc:
        return

    current_sc.withdraw()
    
    try:        # we use try except to ensure code continues even if camera was closed
        face_detection.stop_camera()
    except:
        pass

    if current_sc == process:
        pg.mixer.music.load('Assets/Peaceful_Music.wav')
        pg.mixer.music.stop()
    
    if mode == "P":
        prev_sc.deiconify()
        if prev_sc == process:
            pg.mixer.music.load('Assets/Peaceful_Music.wav')
            pg.mixer.music.play(-1)
    elif mode=="N":
        next_sc.deiconify()
        if next_sc == process:
            pg.mixer.music.load('Assets/Peaceful_Music.wav')
            pg.mixer.music.play(-1)
        elif next_sc==the_end:
            p['value']=0
            p.config(mode='indeterminate')
            the_end.update_idletasks()
            p.start(10)

    else:
        result = tk_messagebox.askquestion("Exit", "Are you sure you exit? (Your data won't be saved...)",
                                           icon='warning')
        if result == 'yes':
            current_sc.withdraw()
            clear_sc()
            animation.draw()
            sc.deiconify()
            if current_sc==process:
                pg.mixer.music.load('Assets/Peaceful_Music.wav')
                pg.mixer.music.stop()
        else:
            current_sc.deiconify()


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
    one_time_only()


def main(type):
    global transaction_type, current_id, img_capt, video_label, detection_error, save_img

    transaction_type = type

    conn = sqlite3.connect('User Profiles/Database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(transaction_type))
    current_id = len(cur.fetchall()) + 1

    sc.withdraw()
    input_sc.deiconify()

    global details_fr, Name_input, Age_input, Gender_o, Contact_Number_input, Email_id_input,\
        Female_o, Consumptions_o, Frequency_o, Address_input, Pulse_rate_input, Blood_group_o, Height_input,\
        Weight_input, Restrictions_o, Female_l, Start_capture, p

    # STEP 1: ENTER GENERAL DATA
    input_sc.title("{} - Let's Start".format(transaction_type))
    input_sc.config(bg="maroon")

    add_menu(prev_sc=sc, current_sc=input_sc, next_sc=img_capt)

    Step1_Frame=Frame(input_sc)
    Step1_Frame.pack()
    Label(Step1_Frame, text="Step 1:", font=('Courier', 30), borderwidth=2, relief="solid").grid(row=0, column=0)
    Label(Step1_Frame, text= 'Fill in to register', font=('Courier', 30)).grid(row=0, column=1)

    details_fr = Listbox(input_sc, bg='pink')
    details_fr.pack(pady=(10, 0), fill=X, padx=15)

    Label(details_fr, text="Name", bg='pink', fg="maroon", font=20, height=1).grid(row=0, column=0, padx=10, pady=10)
    Name_input = Entry(details_fr, bg='pink', fg="maroon", font=20)
    Name_input.grid(row=0, column=1)
    Label(details_fr, text="Age", bg='pink', fg="maroon", font=20, height=1).grid(row=1, column=0, padx=10, pady=10)
    Age_input=Entry(details_fr, bg='pink', fg="maroon", font=20)
    Age_input.grid(row=1, column=1)

    Label(details_fr, text="Gender: ", bg='pink', fg="maroon", font=20, height=1).grid(row=2, column=0, padx=10, pady=(10, 0))
    Gender_o=ttk.Combobox(details_fr, width=18, font=20)
    Gender_o['values'] = ('Male', 'Female')
    Gender_o['state'] = 'readonly'
    Gender_o.grid(column=1, row=2, pady=(10, 0))
    Gender_o.current()

    Label(details_fr, text=''' Did you donate
    blood during the
    last six months: ''', bg='pink', fg="maroon", font=10, height=4).grid(row=3, column=0, padx=10, pady=0)
    Frequency_o = ttk.Combobox(details_fr, width=18, font=20)
    Frequency_o['values'] = ('Yes', 'No')
    Frequency_o['state'] = 'readonly'
    Frequency_o.grid(column=1, row=3)
    Frequency_o.current()

    Label(details_fr, text="Blood Group: ", bg='pink', fg="maroon", font=20, height=1).grid(row=4, column=0, padx=10, pady=10)
    Blood_group_o = ttk.Combobox(details_fr, width=18, font=20)
    Blood_group_o['values'] = ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-')
    Blood_group_o['state'] = 'readonly'
    Blood_group_o.grid(column=1, row=4)
    Blood_group_o.current()

    Label(details_fr, text="Contact Number", bg='pink', fg="maroon", font=20, height=1).grid(row=5, column=0, padx=10, pady=10)
    Contact_Number_input = Entry(details_fr, bg='pink', fg="maroon", font=20)
    Contact_Number_input.grid(row=5, column=1)

    Label(details_fr, text="Email Address", bg='pink', fg="maroon", font=20, height=1).grid(row=6, column=0, padx=10, pady=10)
    Email_id_input = Entry(details_fr, bg='pink', fg="maroon", font=20)
    Email_id_input.grid(row=6, column=1)

    Label(details_fr, text="Home Address", bg='pink', fg="maroon", font=20, height=1).grid(row=7, column=0, padx=10, pady=10)
    Address_input = Entry(details_fr, bg='pink', fg="maroon", font=20)
    Address_input.grid(row=7, column=1)

    Label(details_fr, text="Pulse Rate", bg='pink', fg="maroon", font=20, height=1).grid(row=8, column=0, padx=10, pady=10)
    Pulse_rate_input = Entry(details_fr, bg='pink', fg="maroon", font=20)
    Pulse_rate_input.grid(row=8, column=1)

    Label(details_fr, text="Height (in cm)", bg='pink', fg="maroon", font=20, height=1).grid(row=9, column=0, padx=10, pady=10)
    Height_input = Entry(details_fr, bg='pink', fg="maroon", font=20)
    Height_input.grid(row=9, column=1)

    Label(details_fr, text="Weight (in kg)", bg='pink', fg="maroon", font=20, height=1).grid(row=10, column=0, padx=10, pady=10)
    Weight_input = Entry(details_fr, bg='pink', fg="maroon", font=20)
    Weight_input.grid(row=10, column=1)

    Restrictions_l = Label(details_fr, text="Are you facing: ", bg='pink', fg="maroon", font=20, height=1).grid(row=11, column=0, padx=10, pady=10)
    Restrictions_o = ttk.Combobox(details_fr, width=18, font=20)
    Restrictions_o['values'] = ('(None)', 'Cold', 'Flu', 'Sore Throat', 'Cold Sore', 'Stomach Bug')
    Restrictions_o.grid(column=1, row=11)
    Restrictions_o.current()
    Other_R=Label(details_fr, text='''If you are facing any other infection other than the options of the left menu, type there. 
    If its more than one infection, after each name (except the last) put a comma and space then type''', bg='pink', fg='green')

    Consumptions_l = Label(details_fr, text="Today, have you comsumed:  ", bg='pink', fg="maroon", font=20, height=1).grid(row=12, column=0, padx=10, pady=(10, 0))
    Consumptions_o = ttk.Combobox(details_fr, width=18, font=20)
    Consumptions_o['values'] = ('(None)', 'Alcohol', 'Fatty foods', 'Aspirin', 'Iron Blockers')
    Consumptions_o.grid(column=1, row=12)
    Consumptions_o.current()
    set_gender = Button(details_fr, text="Click me to Confirm Selected Gender",
                        command=lambda: extra_opt(Gender_o.get()), font=20, height=1)
    set_gender.grid(row=2, column=2, padx=(10, 0))
    lbl = Label(details_fr, text='(You can change again)', bg='pink', font=20, height=1)
    lbl.grid(row=2, column=3)

    Female = StringVar()
    Female_l = Label(details_fr, text="Are you: ", bg='pink', fg="maroon", font=20, height=1)
    Female_o = ttk.Combobox(details_fr, width=27, textvariable=Female)
    Female_o['values'] = ('Pregnant', 'Breastfeeding', 'None of the above')
    Frequency_o['state'] = 'readonly'
    Female_o.current()

    Button(input_sc, text="Save Data", command=verify_details).pack()

    # STEP 2: FACE CAPTURE
    img_capt.title('{} - Note for Capturing Face'.format(transaction_type))

    add_menu(prev_sc=input_sc, current_sc=img_capt, next_sc=process)

    Step2_Frame=Frame(img_capt)
    Step2_Frame.pack(pady=10)
    Step2_1 = Label(Step2_Frame, text="Step 2:", font=('Courier', 30), borderwidth=2, relief="solid").grid(row=0, column=0)
    Step2_2=Label(Step2_Frame, text='Capture Your Image', font=('Courier', 30)).grid(row=0, column=1)

    Description = Label(img_capt, font=25, text='''Your webcam will be on and you are requested to take a clear picture of yourself.
                Your whole face should show fully. Try not to cover your face with sunglasses, cap, earmuffs, helmet etc.
                Once the webcam switches on, click 'c' on your keyboard to capture the image...''')
    Description.pack(pady=20)
    
    face_detection.create_widgets(img_capt, transaction_type, current_id)

    # STEP 3: THE PROCESS
    process.title("{} - All the Best!!!".format(transaction_type))

    Step3_Frame = Frame(process)
    Step3_Frame.pack()
    Step3_1 = Label(Step3_Frame, text="Step 3:", font=('Courier', 30), borderwidth=2, relief="solid").grid(row=0, column=0)
    Step3_2 = Label(Step3_Frame, text='The main process', font=('Courier', 30)).grid(row=0, column=1)

    note = Label(process, text='''Now we shall collect your blood. If it is your first time then stay calm! We shall do very carefully. ALL THE BEST!!!''', font=20)
    note.pack(pady=20)

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

    add_menu(prev_sc=process, current_sc=confirm, next_sc=the_end)

    # STEP 5: SAVE DATA & CONCLUDE
    the_end.title('{} - Thank You for Choosing Us!'.format(transaction_type))

    Label(the_end, text='''Now you are done. Thank you for choosing us!
    We hope you come next time; Till then, bye!''',
          font=('bold', 25), fg='blue', bg='light blue').pack()
    Save_All_Data=Button(the_end, text='Save All Data', command=progressbar, bg='lime', font=('bold', 20))
    Save_All_Data.pack(pady=(20, 0))
    p=ttk.Progressbar(the_end, orient=HORIZONTAL, length=500, mode='indeterminate')
    p.pack(pady=20)


def extra_opt(Gender):
    if Gender=='Female':
        Female_l.grid(row=2, column=4, padx=(25, 0))
        Female_o.grid(column=5, row=2, padx=(0, 10))
    else:
        Female_l.grid_forget()
        Female_o.grid_forget()


def one_time_only(destroy=False):
    if destroy:
        result = tk_messagebox.askquestion("Exit", "Are you sure you exit? (Your data won't be saved...)",
                                       icon='warning')
        if result == 'yes':
            animation.draw()
            root.destroy()

    else:
        sc.deiconify()

combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                        settings={'TCombobox':
                                        {'configure':
                                            {'selectbackground': 'blue',
                                            'fieldbackground': 'red',
                                            'background': 'green'
                                            }}}
                        )
combostyle.theme_use('combostyle')

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

screens = [turtle_sc, sc, input_sc, img_capt, process, confirm, the_end]

for i in screens:
    i.withdraw()
    i.geometry(f"{screen_length}x{screen_width}+0+0")
    i.resizable(False, False)
    i.protocol("WM_DELETE_WINDOW", disable_event)

selection=Label(sc, text="What would you like to do?", fg="black", font=('Courier', 50))
selection.place(anchor=CENTER, relx=.5, rely=.1)
sc_fr = Frame(sc)
sc_fr.place(anchor=CENTER, relx=.5, rely=.5)
donate = Button(sc_fr, text="DONATE", fg="lime", bg='dark blue', width=30, height= 6, font=("bold", 20), command=lambda:main('Donors'))
donate.grid(row=0, column=0, padx=(20, 10))
receive = Button(sc_fr, text="RECEIVE", fg="pink", bg='red', width=30, height= 6, font=("bold", 20), command=lambda:main('Receivers'))
receive.grid(row=0, column=2, padx=(10, 20))
Exit = Button(sc_fr, text="EXIT", fg="white", bg='black', width=25, height= 6, font=("bold", 20), command=lambda:one_time_only(True))
Exit.grid(row=0, column=1, padx=10)

animation.draw(turtle_sc, screen_length, screen_width)    # starts animation

sc.deiconify()      # once animation is done, the selection screen shows and from there on, code continues

root.mainloop()
