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

def save_qr():
    global pilqr
    input = textinput.get('1.0', 'end-1c') 
    qr = segno.make(input)
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

left_frame = tk.Frame(root, width=300, bg="lightblue")
left_frame.pack(side="left", fill="both", expand=True)

right_frame = tk.Frame(root, width=300)
right_frame.pack(side="right", fill="both", expand=True)

textinput_frame = tk.Frame(left_frame, height=500)
textinput_frame.pack(anchor=NW)

buttons_frame = tk.Frame(left_frame, height=500)
buttons_frame.pack(anchor=NW, padx=35)

textinput = tk.Text(textinput_frame, height=3, width=40)
textinput.grid(row=0, column=0, padx=5, pady=5)

confirmbutton = tk.Button(buttons_frame, text="Make QR!", command=save_qr)
confirmbutton.grid(row=1, column=0, padx=5, pady=5)

saveqr = tk.Button(buttons_frame, text="Save The QR Code!", command=save_qr_to_disk)
saveqr.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()

