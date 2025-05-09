import os
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import io
import segno
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('qrcode')
root.geometry("1160x650")
root.resizable(width = True, height = True)

home_dir = os.path.expanduser("~")
logo_filepath = None

logosize = 3
is_micro = True
is_warning = False
errorc_level = 'm'

def removelogo():
    global logo_filepath
    logo_filepath = None
    removelogobutton.grid_forget()
    save_qr()

def select_file():
    global logo_filepath
    filetypes = (
        ('PNG files', '*.png'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=home_dir,
        filetypes=filetypes)

    if filename:
        logo_filepath = filename
        save_qr()

def save_qr():
    global pilqr
    global user_qr_input
    global errorc_level
    global is_micro
    global logo_filepath
    user_qr_input = textinput.get('1.0', 'end-1c') 
    if len(user_qr_input) > 14:
        is_micro = False
        microtoggle.config(state=tk.DISABLED, text="Off")
    elif microtoggle.cget("state") == "disabled" and errorc_level != 'h':
        is_micro = True
        microtoggle.config(state=tk.NORMAL, text="On")
    qr = segno.make(user_qr_input, error=errorc_level, boost_error=False)
    if not is_micro:
        qr = segno.make_qr(user_qr_input, error=errorc_level, boost_error=False)
    buffer = io.BytesIO()
    qr.save(buffer, kind='png')
    buffer.seek(0)
    pilqr = Image.open(buffer)
    pilqr = pilqr.resize((250,250), Image.LANCZOS)
    if logo_filepath is not None:
        place_logo()
    else:
        show_qr()

def place_logo():
    global pilqr
    global logo_filepath
    global logosize
    pilqr = pilqr.convert('RGB')
    qr_width, qr_height = pilqr.size
    logo_max_size = qr_height // logosize
    logo_img = Image.open(logo_filepath)
    logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
    box = ((qr_width - logo_img.size[0]) // 2, (qr_height - logo_img.size[1]) // 2)
    pilqr.paste(logo_img, box, mask=logo_img)
    removelogobutton.grid(row=2, column=2, padx=2, sticky=NW)
    show_qr()

def show_qr():
    global pilqr
    global panel
    global warninglabel
    global panel
    global is_warning
    global photoqr
    photoqr = ImageTk.PhotoImage(pilqr)
    if is_warning:
        warninglabel.config(text="⚠ The QR Code might be hard to scan! \nplease check it before you deploy")
    else:
        warninglabel.config(text="")
    panel.config(image = photoqr)

def save_qr_to_disk():
    global pilqr
    pilqr = pilqr.save("QR Code.png")

def toggle_micro():
    global is_micro
    if is_micro:
        is_micro = False
        microtoggle.config(text="Off")
    else:
        is_micro = True
        microtoggle.config(text="On")
    save_qr()

def update_label(val):
    global errorc_level
    index = int(val)
    errorc_value.set(errorc_labels[index])
    errorc_level = errorc_labels_compute[index]
    if errorc_level == 'h':
        is_micro = False
        microtoggle.config(state=tk.DISABLED, text="Off")
    save_qr()

def update_size(val):
    global is_warning
    global logosize
    logosize = float(val)
    if logosize < 3:
        is_warning = True
    else:
        is_warning = False
    save_qr()

def callback(event):
    root.after(1, save_qr)

left_frame = tk.Frame(root, width=500)
left_frame.pack(side="left", fill="both", expand=True)

right_frame = tk.Frame(root, width=300)
right_frame.pack(side="right", fill="both", expand=True)

right_center = tk.Frame(right_frame)
right_center.pack(expan=True)

placeholder = ImageTk.PhotoImage(Image.new('RGB', (100, 100), color = 'gray'))
panel = Label(right_center, image=placeholder)
panel.pack()

warninglabel = tk.Label(right_center, text="", fg='red')
warninglabel.pack()

buttons_frame = tk.Frame(left_frame, height=300)
buttons_frame.grid(row=1, column=0, sticky=NW)

textinput = tk.Text(left_frame, height=3, width=40)
textinput.grid(row=0, column=0, padx=5, pady=5, sticky=NW)

textinput.bind("<Key>", callback)

toggles_frame = tk.Frame(left_frame, height=300)
toggles_frame.grid(row=3, column=0, padx=5, pady=50, sticky=NW)

confirmbutton = tk.Button(buttons_frame, text="Make QR!", command=save_qr)
confirmbutton.grid(row=1, column=0, padx=5, pady=5, sticky=NW)

saveqr = tk.Button(buttons_frame, text="Save The QR Code!", command=save_qr_to_disk)
saveqr.grid(row=1, column=1, padx=5, pady=5)

microtoggle_label = tk.Label(toggles_frame, text="Micro QR Code:")
microtoggle_label.grid(row=0, column=0, padx=5, sticky=NW)

microtoggle = tk.Button(toggles_frame, text="On", command=toggle_micro)
microtoggle.grid(row=0, column=1, padx=5, sticky=NW)

errorc_labels_compute = ['l', 'm', 'q', 'h']
errorc_labels = ['7%', '15%', '25%', '30%']
errorc_value = tk.StringVar()

errorclabels = tk.Label(toggles_frame, text="Error Correction Level:")
errorclabels.grid(row=1,column=0, padx=5)

errorcorrection = tk.Scale(toggles_frame, from_=0, to=3,orient='horizontal', command=update_label, showvalue=0)
errorcorrection.grid(row=1, column=1, padx=1, sticky=W)

label = tk.Label(toggles_frame, textvariable=errorc_value)
label.grid(row=1, column=2, padx=5, pady=5, sticky=NW)

errorc_value.set(errorc_labels[0])

logolabel = tk.Label(toggles_frame, text="Add A Logo: ")
logolabel.grid(row=2, column=0, padx=5, pady=5, sticky=NW)

logobutton = tk.Button(toggles_frame, text="Open file", command=select_file)
logobutton.grid(row=2, column=1, padx=5, sticky=NW)

removelogobutton = tk.Button(toggles_frame, text="Remove Logo", command=removelogo)

logosizelabel = tk.Label(toggles_frame, text="Logo Size: ")
logosizelabel.grid(row=3, column=0, pady=5, padx=5, sticky=NW)

defaultlogosize = tk.DoubleVar(value=3)

logosizescale = tk.Scale(toggles_frame, variable=defaultlogosize, from_=1, to=5, resolution=0.5, orient='horizontal', showvalue=0, command=update_size)
logosizescale.grid(row=3, column=1, padx=5, pady=5, sticky=W)

root.mainloop()
