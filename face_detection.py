import cv2
from tkinter import *
from PIL import Image, ImageTk

proceed_to_next = False

def initialize():
    global frame, capturing, webcam, face_detect_sample, coordinates
    for i in range(3):
        Start_capture.flash()

    capturing = True
    webcam = cv2.VideoCapture(0)
    Start_capture.configure(text="Click to capture", command=lambda:stop_camera("save"))

    detection_error.configure(text="")
    save_btn.grid_forget()
    save_btn.configure(text="Save Capture")
    coordinates = None

    face_detect_sample = cv2.CascadeClassifier("Assets/haarcascade_frontalface_alt.xml")

    update_frame()


def update_frame():
    global coordinates, frame

    if capturing == "save": # saves and closes camera
        crop_preview()
        return
    
    if not capturing:   # simply closes camera
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
    global cropped
    try:
        (x1, y1), (x2, y2) = coordinates
        cropped = frame[y1:y2, x1:x2]
    except:
        cropped = frame     # if face wasn't detecting, the frame will be untouched
        detection_error.configure(text="Unable to detect face, you can either proceed or retake")
    
    rgb_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_cropped)
    imgtk = ImageTk.PhotoImage(image=img, master=video_label)
    video_label.imgtk = imgtk  # keep a reference so it isn't garbage collected
    video_label.configure(image=imgtk)
        
    save_btn.grid(row=1, column=0)

def stop_camera(mode=False):    # mode can be either "save", True or False
    global capturing
    capturing = mode
    webcam.release()

    Start_capture.configure(text="Click to Start Camera", command=initialize)


def save_img(transaction_type, current_id):
    global proceed_to_next
    cv2.imwrite('User Profiles/{}/ID_[{}].png'.format(transaction_type, current_id), cropped)
    save_btn.configure(text="Capture Saved Successfuly!")
    proceed_to_next = True


def create_widgets(sc, transaction_type, current_id):
    global Start_capture, save_btn, detection_error, video_label
    Start_capture = Button(sc, text='Click to Start Camera', command=initialize, width=45,
                               font=("Segoe UI", 15, "bold"), activebackground='blue',activeforeground='white', fg='black', bg='lightgreen')
    Start_capture.pack()

    horizontal_layout = Frame(sc, bg="maroon")
    horizontal_layout.pack()

    video_label = Label(horizontal_layout, bg="maroon")
    video_label.grid(row=0, column=0, pady=10)

    vertical_layout = Frame(horizontal_layout, bg="maroon")
    vertical_layout.grid(row=0, column=1, padx=10)
    
    save_btn = Button(vertical_layout, text="Save Capture", bg="lightgreen", font=("Segoe UI", 15), command=lambda:save_img(transaction_type, current_id))

    detection_error = Label(vertical_layout, text="", fg="pink", bg="maroon", font=("Segoe UI", 15))
    detection_error.grid(row=0, column=0)
