from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
keyboard = Frame(root, padx=5, pady=5, bg="grey")
keyboard.grid(row=0, column=0, sticky=NSEW)

keyboard.grid_rowconfigure(0, weight=1)
keyboard.grid_columnconfigure(0, weight=1)
keyboard.grid_columnconfigure(1, weight=1)
keyboard.grid_columnconfigure(2, weight=1)
keyboard.grid_columnconfigure(3, weight=1)


def buttonExitclick():
    root.destroy()


def buttonStartclick():
    if start_button["background"] == 'green':
        start_button["background"] = "yellow"
        start_button.configure(state="disabled")


def buttonStopclick():
    if start_button["background"] == "yellow":
        start_button["background"] = "green"
        start_button.configure(state="normal")


start_button = Button(keyboard, command=buttonStartclick, padx=5, pady=5, text='Start', background='green')
start_button.grid(row=0, column=0, pady=25 , padx=25,sticky='EWNS')
stop_button = Button(keyboard, command=buttonStopclick, padx=5, pady=5, text='Stop', background='red')
stop_button.grid(row=0, column=1, pady=25, padx=25, sticky='EWNS')
reset_button = Button(keyboard, padx=5, pady=5, text='Reset', background='red')
reset_button.grid(row=0, column=2, pady=25, padx=25, sticky='EWNS')
exit_button = Button(keyboard, command=buttonExitclick, padx=5, pady=5, text='Exit')
exit_button.grid(row=0, column=3, pady=25, padx=25, sticky='EWNS')

progress = ttk.Progressbar(keyboard, mode='determinate', length=300)
progress.grid(column=0, columnspan=4, row=2, padx=5, pady=25, sticky='EWNS')

Label(keyboard, text="X", background= 'grey').grid(column=0, row=3, sticky='EWNS', padx=5, pady=15)
Label(keyboard, text="Y", background= 'grey').grid(column=0, row=4, sticky='EWNS', padx=5, pady=15)
Label(keyboard, text="Z", background= 'grey').grid(column=0, row=5, sticky='EWNS', padx=5, pady=15)

Label(keyboard, text="RX", background= 'grey').grid(column=2, row=3, sticky='EWNS', padx=5, pady=15)
Label(keyboard, text="RY", background= 'grey').grid(column=2, row=4, sticky='EWNS', padx=5, pady=15)
Label(keyboard, text="RZ", background= 'grey').grid(column=2, row=5, sticky='EWNS', padx=5, pady=15)

myX = "5,55"
myY = "6,66"
myZ = "7,77"

Label(keyboard, text=myX, background="white", relief=SUNKEN, padx=20).grid(column=1, row=3, sticky='EWNS')
Label(keyboard, text=myY, background="white", relief=SUNKEN, padx=20).grid(column=1, row=4, sticky='EWNS')
Label(keyboard, text=myZ, background="white", relief=SUNKEN, padx=20).grid(column=1, row=5, sticky='EWNS')

myRX = "8,88"
myRY = "9,99"
myRZ = "1,11"
Label(keyboard, text=myRX, background="white", relief=SUNKEN, padx=20).grid(column=3, row=3, sticky='EWNS')
Label(keyboard, text=myRY, background="white", relief=SUNKEN, padx=20).grid(column=3, row=4, sticky='EWNS')
Label(keyboard, text=myRZ, background="white", relief=SUNKEN, padx=20).grid(column=3, row=5, sticky='EWNS')

root.attributes('-fullscreen', True)
root.mainloop()
