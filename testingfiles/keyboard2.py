from tkinter import *
import tkinter

Keyboard_App = tkinter.Tk()
Keyboard_App.title("Keyboard")
Keyboard_App.resizable(0, 0)


def select(value):
    if value == "<-":
        entry2 = entry.get()
        pos = entry2.find("")
        pos2 = entry2[pos:]
        entry.delete(pos2, tkinter.END)
    elif value == " Space ":
        entry.insert(tkinter.END, ' ')
    elif value == " Tab ":
        entry.insert(tkinter.END, '    ')
    else:
        entry.insert(tkinter.END, value)


buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Backspace',
           'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
           'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', "Enter",
           "Shift", 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', '>', '?', "Shift"
]
label1 = Label(Keyboard_App, text='            ').grid(row=0, columnspan=1)
entry = Entry(Keyboard_App, width=128)
entry.grid(row=1, columnspan=15)

varRow = 2
varColumn = 0

for button in buttons:

    command = lambda x=button: select(x)
    if button != " Space ":
        tkinter.Button(Keyboard_App, text=button, width=5, bg="#000000", fg="#ffffff",
                       activebackground="#ffffff", activeforeground="#000000", relief='raised', padx=4,
                       pady=4, bd=4, command=command).grid(row=varRow, columnspan=varColumn)
    if button == " Space ":
        tkinter.Button(Keyboard_App, text=button, width=60, bg="#000000", fg="#ffffff",
                       activebackground="#ffffff", activeforeground="#000000", relief='raised', padx=4,
                       pady=4, bd=4, command=command).grid(row=6, columnspan=16)

    varColumn += 1
    if varColumn > 14 and varRow == 2:
        varColumn = 0
        varRow += 1
    if varColumn > 14 and varRow == 3:
        varColumn = 0
        varRow += 1

Keyboard_App.mainloop()
