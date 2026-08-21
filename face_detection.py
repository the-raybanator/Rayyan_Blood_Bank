import cv2
from PIL import Image, ImageTk
from tkinter import *

def initialize():
    global frame, capturing, webcam, face_detect_sample, coordinates
    for i in range(3):
        Start_capture.flash()

    capturing = True
    webcam = cv2.VideoCapture(0)
    Start_capture.configure(text="Click to capture", command=stop_camera)

    detection_error.configure(text="")
    save_img.pack_forget()
    coordinates = None

    face_detect_sample = cv2.CascadeClassifier("Assets/haarcascade_frontalface_alt.xml")

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

    Start_capture.configure(text="Click to Start Camera", command=initialize)

def create_widgets(sc, transaction_type, current_id):
    global Start_capture, save_img, detection_error, video_label
    Start_capture = Button(sc, text='Click me to open webcam', command=initialize, width=70,
                               font=('bold', 25), activebackground='blue',activeforeground='white', fg='black', bg='lime')
    Start_capture.pack()
    
    video_label = Label(sc)
    video_label.pack(pady=10)
    
    detection_error = Label(sc, text="", fg="red", font=("Arial", 15))
    detection_error.pack()
    
    save_img = Button(sc, text="Save and Proceed", bg="lime", font=("Arial", 15), command=lambda:cv2.imwrite('User Profiles/{}/ID_[{}].png'.format(transaction_type, current_id), frame))

