from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import io
import segno
import tkinter

root = tk.Tk()
root.title('qrcode')
root.geometry("1160x650")
root.resizable(width = True, height = True)

is_micro = True

def save_qr():
    global pilqr
    global user_qr_input
    global is_micro
    user_qr_input = textinput.get('1.0', 'end-1c') 
    if len(user_qr_input) > 14:
        is_micro = False
        microtoggle.config(state=tk.DISABLED, text="Off")
    elif microtoggle.cget("state") == "disabled":
        is_micro = True
        microtoggle.config(state=tk.NORMAL, text="On")
    qr = segno.make(user_qr_input)
    if not is_micro:
        qr = segno.make_qr(user_qr_input)
    qr.mask
    buffer = io.BytesIO()
    qr.save(buffer, kind='png')
    buffer.seek(0)
    pilqr = Image.open(buffer)
    show_qr()

def show_qr():
    global pilqr
    pilqr = pilqr.resize((250,250), Image.LANCZOS)
    photoqr = ImageTk.PhotoImage(pilqr)
    panel = Label(right_frame, image=photoqr)
    panel.image = photoqr
    panel.place(relx=.5, rely=.5, anchor="c")

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

left_frame = tk.Frame(root, width=300)
left_frame.pack(side="left", fill="both", expand=True)

right_frame = tk.Frame(root, width=300)
right_frame.pack(side="right", fill="both", expand=True)

buttons_frame = tk.Frame(left_frame, height=300)
buttons_frame.grid(row=1, column=0)

textinput = tk.Text(left_frame, height=3, width=40)
textinput.grid(row=0, column=0, padx=5, pady=5)

toggles_frame = tk.Frame(left_frame, height=300)
toggles_frame.grid(row=3, column=0, padx=5, pady=50, sticky=NW)

confirmbutton = tk.Button(buttons_frame, text="Make QR!", command=save_qr)
confirmbutton.grid(row=1, column=0, padx=5, pady=5)

saveqr = tk.Button(buttons_frame, text="Save The QR Code!", command=save_qr_to_disk)
saveqr.grid(row=1, column=1, padx=5, pady=5)

microtoggle_label = tk.Label(toggles_frame, text="Micro QR Code:")
'1-Q'
microtoggle_label.grid(row=0, column=0, padx=5, sticky=NW)

microtoggle = tk.Button(toggles_frame, text="On", command=toggle_micro)
microtoggle.grid(row=0, column=1, padx=5, sticky=NW)

root.mainloop()
#test ssh 
