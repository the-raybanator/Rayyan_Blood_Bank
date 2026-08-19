from turtle import RawTurtle, TurtleScreen
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tk_messagebox
import os
import time
import cv2
import datetime
import pygame
from pygame import mixer
import sqlite3
from PIL import Image, ImageTk

pygame.init()
original_dir = os.getcwd()


def disable_event():
   pass


def Graphic_Design():
    global turtle_sc
    turtle_sc.deiconify()
    t.hideturtle()
    b.hideturtle()
    b.penup()
    b.goto(-260, -230)
    b.lt(90)
    b.showturtle()
    b.speed(1)
    b.bk(100)

    fly_to(-190, 150, t)
    t.pencolor('blue')
    t.showturtle()
    t.write("RAYYAN - ", font=('courier', 35, 'bold'))
    t.pencolor('red')
    fly_to(50, 160, t)
    t.write("Your gateway to", font=('courier', 25))
    fly_to(70, 130, t)
    t.write("donate blood", font=('courier', 25))
    fly_to(-100, 30, t)
    t.pencolor("blue")
    t.pensize(3)
    t.write('Give the gift of life', font=('arial', 25))
    fly_to(-70, -35, t)
    t.write("Donate blood!", font=('arial', 25))
    time.sleep(1) #On final make it 4 seconds
    t.reset()
    b.reset()
    turtle_sc.withdraw()


def fly_to(x, y, turtle_):
    if turtle_ == t:
        t.penup()
        t.goto(x, y)
        t.pendown()
    else:
        b.penup()
        b.goto(x, y)
        b.pendown()


def get_rows():
    conn = sqlite3.connect('Rayyan_Blood_Donation/Database.db')
    cur = conn.cursor()

    if transaction_type == "Donation":
        os.chdir('Rayyan_Blood_Donation/Donator')
    else:
        os.chdir('Rayyan_Blood_Donation/Recieve')

    cur.execute("SELECT * FROM {}".format(transaction_type))

    cv2.imwrite('ID_[{}].png'.format(current_id), frame)
    os.chdir(original_dir)


def capt_img():
    global frame, capturing, webcam, face_detect_sample, coordinates
    for i in range(3):
        Start_capture.flash()

    capturing = True
    webcam = cv2.VideoCapture(0)
    Start_capture.configure(text="Click to capture", command=stop_camera)

    detection_error.configure(text="")
    save_img.pack_forget()
    coordinates = None

    face_detect_sample = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

    update_frame()


def update_frame():
    global coordinates, frame

    if not capturing:
        crop_preview()
        return

    ret, frame = webcam.read()
    if ret:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detect_face = face_detect_sample.detectMultiScale(gray_frame, 1.05, 3)
        for (x, y, w, h) in detect_face:
            coordinates = ((x-10, y-40), (x + w + 10, y + h + 10))      # top left corner and bottom right corner of a rectangle
            cv2.rectangle(frame, coordinates[0], coordinates[1], (255, 255, 255), 1)
            

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img, master=video_label)

        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    video_label.after(15, update_frame)  # ~66 fps cap; schedules the next call


def crop_preview():
    try:
        (x1, y1), (x2, y2) = coordinates
        cropped = frame[y1:y2, x1:x2]

        rgb_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_cropped)
        imgtk = ImageTk.PhotoImage(image=img, master=video_label)
        video_label.imgtk = imgtk  # keep a reference so it isn't garbage collected
        video_label.configure(image=imgtk)
    except:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img, master=video_label)
        
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        detection_error.configure(text="Unable to detect face, you can either proceed or retake")
        
    save_img.pack()

def stop_camera():
    global capturing
    capturing = False
    webcam.release()

    Start_capture.configure(text="Click to Start Camera", command=capt_img)

def add_exit_prior_step_btn(prev_sc, next_sc, current_sc):
    global next_step_recurring, exit_prior_step_fr
    exit_prior_step_fr=Frame(current_sc)
    exit_prior_step_fr.pack(side=BOTTOM, pady=10, anchor=CENTER)
    #SUB_FR=Frame(exit_prior_step_fr, relief='sunken', bg='lime', borderwidth=5)
    #SUB_FR.grid(row=0, column=0)
    #Label(SUB_FR, text='SAVE AND GO TO -', font='bold', bg='lime', fg='purple').grid(row=0, column=0)
    prior_step_recurring = Button(exit_prior_step_fr, text="Previous Step", fg="red", bg="white", font="bold", command=lambda:change_sc(prev_sc=prev_sc, current_sc=current_sc, mode="P", next_sc=0)).grid(padx=5, row=0, column=0, pady=5)
    next_step_recurring = Button(exit_prior_step_fr, text="Next Step", fg="red", bg="lime", font="bold", command=lambda:change_sc(next_sc=next_sc, current_sc=current_sc, mode="N", prev_sc=0))
    next_step_recurring.grid(padx=5, row=0, column=1, pady=5)
    if current_sc!=img_capt:
        next_step_recurring.grid(padx=5, row=0, column=1, pady=5)
        if bool(next_step_recurring.winfo_ismapped()) == True:
           next_step_recurring.grid_forget()
    Exit_recurring = Button(exit_prior_step_fr, text="Exit", fg="red", bg="white", font="bold", command=lambda:change_sc(current_sc=current_sc, mode="E", prev_sc=0, next_sc=0)).grid(padx=5, row=0, column=2)
    if current_sc==sc_donate_collect:
        restart_recurring = Button(exit_prior_step_fr, text="Clear", fg="red", bg="white", font="bold",
                                   command=lambda:clear_sc(0)).grid(padx=5, row=0, column=3)

def clear_sc(stat):
    if stat==0:
        result = tk_messagebox.askquestion("Clear Data", '''Are you sure you want to clear all the data in this screen?
        (Your data won't be saved...)''', icon='warning')
        if result == 'yes':
            clear_sc(1)

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
            sc_donate_collect.withdraw()
            tk_messagebox.showinfo("Information", "Sorry... You cannot donate blood asyou are above 65 years of age. ")
            error = 1
            return()
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
        change_sc(0, img_capt, sc_donate_collect, 'N')

def show_data():
    global Name_c, Age_c, Gender_c, Female_c, Frequency_c, Blood_group_c, Contact_Number_c, Email_id_c, Pulse_rate_c,\
        Height_c, Weight_c, Restrictions_c, Consumptions_c
    Step4_1 = Label(Step4_Frame, text="Step 4:", font=('Courier', 30), borderwidth=2, relief="solid").grid(row=0, column=0)
    Step4_2 = Label(Step4_Frame, text='Confirm Your Details', font=('Courier', 30)).grid(row=0, column=1)
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
def change_sc(prev_sc, next_sc, current_sc, mode):
    if mode!='E' or next_sc!=img_capt or prev_sc!=sc:
        current_sc.withdraw()
    if mode=="P":
        prev_sc.deiconify()
        if prev_sc==process:
            os.chdir('Rayyan_Blood_Donation')
            mixer.music.load('Peaceful_Music.wav')
            mixer.music.play(-1)
        elif img_capt==prev_sc:
            os.chdir('Rayyan_Blood_Donation')
            mixer.music.load('Peaceful_Music.wav')
            mixer.music.stop()
            Start_capture.flash()
    elif mode=="N":
        next_sc.deiconify()
        if next_sc==sc_donate_collect:
            skip_this_fun=1
        if next_sc!=img_capt:
            next_sc.deiconify()
        if next_sc==process:
            mixer.music.load('Peaceful_Music.wav')
            mixer.music.play(-1)
        elif next_sc==confirm:
            mixer.music.load('Peaceful_Music.wav')
            mixer.music.stop()
            show_data()
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
            clear_sc('no_asking')
            Graphic_Design()
            sc.deiconify()
            if current_sc==process:
                os.chdir('Rayyan_Blood_Donation')
                mixer.music.load('Peaceful_Music.wav')
                mixer.music.stop()
        else:
            current_sc.deiconify()

def sc_show():
    notification.withdraw()
    sc_donate_collect.deiconify()


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(photo):
    os.chdir('Rayyan_Blood_Donation')
    conn = sqlite3.connect('Database.db')
    cursor = conn.cursor()
    empPhoto = convertToBinaryData(photo)
    lst=[current_id, Name_c.get(), Age_c.get(), Gender_c.get(), Female_c.get(), Frequency_c.get(), Blood_group_c.get(),
     Contact_Number_c.get(), Email_id_c.get(), Pulse_rate_c,
     Height_c, Weight_c, Restrictions_c, Consumptions_c, empPhoto]

    conn.execute('''INSERT INTO Donation(UNIQUE_ID, NAME, AGE, GENDER, FEMALE_CONDITIONS, LAST, BLOOD_GROUP, CONTACT_NUMBER, EMAIL_ID, PULSE_RATE, 
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

    os.chdir(original_dir)
    if transaction_type == "Donation":
        os.chdir('Rayyan_Blood_Donation/Donator')
    else:
        os.chdir('Rayyan_Blood_Donation/Recieve')

    insertBLOB('Rayyan_Blood_Donation/{}\ID_[{}].png'.format(transaction_type, current_id), transaction_type)
    one_time_only(1)

def common(type):
    global transaction_type, current_id, img_capt, video_label, detection_error, save_img

    transaction_type = type

    os.chdir('Rayyan_Blood_Donation')
    conn = sqlite3.connect('Database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(transaction_type))
    current_id = len(cur.fetchall()) + 1


    hide_img=True
    sc.withdraw()
    global sc_donate_collect, details_fr, Name_input, Age_input, Gender_o, Contact_Number_input, Email_id_input,\
        Female_o, Consumptions_o, Frequency_o, Address_input, Pulse_rate_input, Blood_group_o, Height_input,\
        Weight_input, Restrictions_o, Female_l, notification, Start_capture, p, the_end

    notification = Toplevel(root)
    notification.geometry('1200x200+50+20')
    notification.protocol("WM_DELETE_WINDOW", disable_event)
    notification.resizable(False, False)
    notification.title('Notification')

    os.chdir(original_dir)
    pic1=Canvas(master=notification, width = 200, height = 200, bg='white')
    pic1.pack(side=LEFT)
    pic_screen1 = TurtleScreen(pic1)
    pic_screen1.register_shape('Info_Icon.gif')
    draw1 = RawTurtle(pic_screen1)
    draw1.shape('Info_Icon.gif')
    draw1.goto(0, 0)

    Label(notification, text='''In the whole software, If you need to input any other
    input which is not in the options of the menu, then you can directly type there (like an entry). If you need
    to input more than one item, after each name (except the last) put a comma and space then type.''', font=20).pack()
    Button(notification, text='Okay', command=sc_show, font=25, width=20).pack(pady=10)

    sc_donate_collect = Toplevel(root)
    sc_donate_collect.withdraw()
    sc_donate_collect.geometry('1450x790+50+0')
    confirm.geometry('1450x800+50+0')
    sc_donate_collect.resizable(False, False)
    sc_donate_collect.protocol("WM_DELETE_WINDOW", disable_event)
    sc_donate_collect.title("{} - Let's Start".format(transaction_type))
    Step1_Frame=Frame(sc_donate_collect)
    Step1_Frame.pack()
    Label(Step1_Frame, text="Step 1:", font=('Courier', 30), borderwidth=2, relief="solid").grid(row=0, column=0)
    Label(Step1_Frame, text= 'Fill in to register', font=('Courier', 30)).grid(row=0, column=1)

    details_fr = Listbox(sc_donate_collect, bg='yellow')
    details_fr.pack(pady=(10, 0), fill=X, padx=15)

    Label(details_fr, text="Name", bg='yellow', fg="blue", font=20, height=1).grid(row=0, column=0, padx=10, pady=10)
    Name_input=Entry(details_fr, bg='pink', fg="blue", font=20)
    Name_input.grid(row=0, column=1)
    Label(details_fr, text="Age", bg='yellow', fg="blue", font=20, height=1).grid(row=1, column=0, padx=10, pady=10)
    Age_input=Entry(details_fr, bg='pink', fg="blue", font=20)
    Age_input.grid(row=1, column=1)

    Label(details_fr, text="Gender: ", bg='yellow', fg="blue", font=20, height=1).grid(row=2, column=0, padx=10, pady=(10, 0))
    Gender_o=ttk.Combobox(details_fr, width=18, font=20)
    Gender_o['values'] = ('Male', 'Female')
    Gender_o['state'] = 'readonly'
    Gender_o.grid(column=1, row=2, pady=(10, 0))
    Gender_o.current()

    Label(details_fr, text=''' Did you donate
    blood during the
    last six months: ''', bg='yellow', fg="blue", font=10, height=4).grid(row=3, column=0, padx=10, pady=0)
    Frequency_o = ttk.Combobox(details_fr, width=18, font=20)
    Frequency_o['values'] = ('Yes', 'No')
    Frequency_o['state'] = 'readonly'
    Frequency_o.grid(column=1, row=3)
    Frequency_o.current()

    Label(details_fr, text="Blood Group: ", bg='yellow', fg="blue", font=20, height=1).grid(row=4, column=0, padx=10, pady=10)
    Blood_group_o = ttk.Combobox(details_fr, width=18, font=20)
    Blood_group_o['values'] = ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-')
    Blood_group_o['state'] = 'readonly'
    Blood_group_o.grid(column=1, row=4)
    Blood_group_o.current()

    Label(details_fr, text="Contact Number", bg='yellow', fg="blue", font=20, height=1).grid(row=5, column=0, padx=10, pady=10)
    Contact_Number_input = Entry(details_fr, bg='pink', fg="blue", font=20)
    Contact_Number_input.grid(row=5, column=1)
    Label(details_fr, text="Email Address", bg='yellow', fg="blue", font=20, height=1).grid(row=6, column=0, padx=10, pady=10)
    Email_id_input = Entry(details_fr, bg='pink', fg="blue", font=20)
    Email_id_input.grid(row=6, column=1)
    Label(details_fr, text="Home Address", bg='yellow', fg="blue", font=20, height=1).grid(row=7, column=0, padx=10, pady=10)
    Address_input = Entry(details_fr, bg='pink', fg="blue", font=20)
    Address_input.grid(row=7, column=1)

    Label(details_fr, text="Pulse Rate", bg='yellow', fg="blue", font=20, height=1).grid(row=8, column=0, padx=10, pady=10)
    Pulse_rate_input = Entry(details_fr, bg='pink', fg="blue", font=20)
    Pulse_rate_input.grid(row=8, column=1)
    Label(details_fr, text="Height (in cm)", bg='yellow', fg="blue", font=20, height=1).grid(row=9, column=0, padx=10, pady=10)
    Height_input = Entry(details_fr, bg='pink', fg="blue", font=20)
    Height_input.grid(row=9, column=1)
    Label(details_fr, text="Weight (in kg)", bg='yellow', fg="blue", font=20, height=1).grid(row=10, column=0, padx=10, pady=10)
    Weight_input = Entry(details_fr, bg='pink', fg="blue", font=20)
    Weight_input.grid(row=10, column=1)

    Restrictions_l = Label(details_fr, text="Are you facing: ", bg='yellow', fg="blue", font=20, height=1).grid(row=11, column=0, padx=10, pady=10)
    Restrictions_o = ttk.Combobox(details_fr, width=18, font=20)
    Restrictions_o['values'] = ('(None)', 'Cold', 'Flu', 'Sore Throat', 'Cold Sore', 'Stomach Bug')
    Restrictions_o.grid(column=1, row=11)
    Restrictions_o.current()
    Other_R=Label(details_fr, text='''If you are facing any other infection other than the options of the left menu, type there. 
    If its more than one infection, after each name (except the last) put a comma and space then type''', bg='yellow', fg='green')

    Consumptions_l = Label(details_fr, text="Today, have you comsumed:  ", bg='yellow', fg="blue", font=20, height=1).grid(row=12, column=0, padx=10, pady=(10, 0))
    Consumptions_o = ttk.Combobox(details_fr, width=18, font=20)
    Consumptions_o['values'] = ('(None)', 'Alcohol', 'Fatty foods', 'Aspirin', 'Iron Blockers')
    Consumptions_o.grid(column=1, row=12)
    Consumptions_o.current()
    set_gender = Button(details_fr, text="Click me to Confirm Selected Gender",
                        command=lambda: extra_opt(Gender_o.get()), font=20, height=1)
    set_gender.grid(row=2, column=2, padx=(10, 0))
    lbl = Label(details_fr, text='(You can change again)', bg='yellow', font=20, height=1)
    lbl.grid(row=2, column=3)

    Female = StringVar()
    Female_l = Label(details_fr, text="Are you: ", bg='yellow', fg="blue", font=20, height=1)
    Female_o = ttk.Combobox(details_fr, width=27, textvariable=Female)
    Female_o['values'] = ('Pregnant', 'Breastfeeding', 'None of the above')
    Frequency_o['state'] = 'readonly'
    Female_o.current()

    img_capt.title('{} - Note for Capturing Face'.format(transaction_type))

    Step2_Frame=Frame(img_capt)
    Step2_Frame.pack(pady=10)
    Step2_1 = Label(Step2_Frame, text="Step 2:", font=('Courier', 30), borderwidth=2, relief="solid").grid(row=0, column=0)
    Step2_2=Label(Step2_Frame, text='Capture Your Image', font=('Courier', 30)).grid(row=0, column=1)

    Description = Label(img_capt, font=25, text='''Your webcam will be on and you are requested to take a clear picture of yourself.
                Your whole face should show fully. Try not to cover your face with sunglasses, cap, earmuffs, helmet etc.
                Once the webcam switches on, click 'c' on your keyboard to capture the image...''')
    Description.pack(pady=20)
    
    Start_capture = Button(img_capt, text='Click me to open webcam', command=capt_img, width=70,
                           font=('bold', 25), activebackground='blue',activeforeground='white', fg='black', bg='lime')
    Start_capture.pack()

    video_label = Label(img_capt)
    video_label.pack(pady=10)

    detection_error = Label(img_capt, text="", fg="red", font=("Arial", 15))
    detection_error.pack()

    save_img = Button(img_capt, text="Save and Proceed", bg="lime", font=("Arial", 15), command=get_rows)

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
    pic_screen.register_shape('good_luck.gif')
    draw = RawTurtle(pic_screen)
    draw.shape('good_luck.gif')
    draw.goto(0, 0)

    add_exit_prior_step_btn(prev_sc=img_capt, current_sc=process, next_sc=confirm)

    confirm.title('{} - One Last Step to go'.format(transaction_type))
    the_end = Toplevel()
    the_end.title('{} - Thank You for Choosing Us!'.format(transaction_type))
    the_end.withdraw()
    the_end.geometry('1050x450+250+220')
    the_end.resizable(False, False)
    the_end.protocol("WM_DELETE_WINDOW", disable_event)
    Label(the_end, text='''Now you are done. Thank you for choosing us!
    We hope you come next time; Till then, bye!''',
          font=('bold', 25), fg='blue', bg='light blue').pack()
    Save_All_Data=Button(the_end, text='Save All Data', command=progressbar, bg='lime', font=('bold', 20))
    Save_All_Data.pack(pady=(20, 0))
    p=ttk.Progressbar(the_end, orient=HORIZONTAL, length=500, mode='indeterminate')
    p.pack(pady=20)

    add_exit_prior_step_btn(prev_sc=process, current_sc=confirm, next_sc=the_end)
    add_exit_prior_step_btn(prev_sc=sc_donate_collect, current_sc=img_capt, next_sc=process)
    add_exit_prior_step_btn(prev_sc=sc, current_sc=sc_donate_collect, next_sc=img_capt)

def extra_opt(Gender):
    if Gender=='Female':
        Female_l.grid(row=2, column=4, padx=(25, 0))
        Female_o.grid(column=5, row=2, padx=(0, 10))
    else:
        Female_l.grid_forget()
        Female_o.grid_forget()


def one_time_only(n):
    if n==0:
        result = tk_messagebox.askquestion("Exit", "Are you sure you exit? (Your data won't be saved...)",
                                       icon='warning')
        if result == 'yes':
            sc.destroy()
            Graphic_Design()

    else:
        Graphic_Design()
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
hide_img=True

root = Tk()
root.withdraw()

turtle_sc = Toplevel(root)
turtle_sc.protocol("WM_DELETE_WINDOW", disable_event)
turtle_sc.geometry('800x500+150+50')
turtle_sc.resizable(False, False)
turtle_sc.title('Rayyan Blood Donations')
canvas=Canvas(master = turtle_sc, width = 800, height = 500)
canvas.grid(padx=2, pady=2, row=0, column=0, rowspan=10, columnspan=10)
screen = TurtleScreen(canvas)
screen.register_shape('giphy.gif')
t = RawTurtle(screen)
b = RawTurtle(screen)
b.shape('giphy.gif')
turtle_sc.withdraw()

sc = Toplevel(root)
sc.resizable(False, False)
sc.protocol("WM_DELETE_WINDOW", disable_event)
sc.title('Select Your Action')
sc.geometry('1500x650')
sc.withdraw()

selection=Label(sc, text="What would you like to do?", fg="black", font=('Courier', 50))
selection.place(anchor=CENTER, relx=.5, rely=.1)
sc_fr = Frame(sc)
sc_fr.place(anchor=CENTER, relx=.5, rely=.5)
donate = Button(sc_fr, text="DONATE", fg="lime", bg='dark blue', width=30, height= 6, font=("bold", 20), command=lambda:common('Donations'))
donate.grid(row=0, column=0, padx=(20, 10))
recieve = Button(sc_fr, text="RECIEVE", fg="yellow", bg='red', width=30, height= 6, font=("bold", 20), command=lambda:common('Recieve'))
recieve.grid(row=0, column=2, padx=(10, 20))
Exit = Button(sc_fr, text="EXIT", fg="white", bg='black', width=25, height= 6, font=("bold", 20), command=lambda:one_time_only(0))
Exit.grid(row=0, column=1, padx=10)

img_capt = Toplevel(root)
img_capt.geometry('1050x850+250+220')
img_capt.resizable(False, False)
img_capt.protocol("WM_DELETE_WINDOW", disable_event)
img_capt.withdraw()

confirm = Toplevel(root)
Step4_Frame = Frame(confirm)
Step4_Frame.pack()
confirm.protocol("WM_DELETE_WINDOW", disable_event)
confirm.resizable(False, False)
confirm.withdraw()

process = Toplevel(root)
process.geometry('1050x390+250+220')
process.resizable(False, False)
process.protocol("WM_DELETE_WINDOW", disable_event)
process.withdraw()

confirm_fr = Frame(confirm)
confirm_fr.pack()
Label(confirm, text='Below are all the details you mentioned. Kindly check if they are correct as we shall record them!', font=25).pack(pady=10)

Graphic_Design()
sc.deiconify()

root.mainloop()