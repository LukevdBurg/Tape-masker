import tkinter.ttk as ttk
from tkinter import *


class MyApp:
    def __init__(self, parent):

        # ---Button constants---
        button_width = 6

        button_padx = "4m"
        button_pady = "1m"

        buttons_frame_padx = "3m"
        buttons_frame_pady = "2m"
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"
        # ---End of constants---

        self.myParent = parent
        self.myParent.geometry("640x400")

        self.myContainer1 = Frame(parent)
        self.myContainer1.pack(expand=YES, fill=BOTH)

        # ---Button frame ---
        self.button_frame = Frame(self.myContainer1, borderwidth=5, background='grey')
        self.button_frame.pack(fill=X)

        self.button1 = Button(self.button_frame, command=self.button1Click)
        self.button1.configure(text="Start!", background="green")
        self.button1.configure(
            width=button_width,
            padx=button_padx,
            pady=button_pady
        )
        self.button1.pack(side=LEFT)
        self.button1.bind("<Return>", self.button1Click_a)

        self.button2 = Button(self.button_frame, command=self.button2Click)
        self.button2.configure(text="Stop!", background="red")
        self.button2.configure(
            width=button_width,
            padx=button_padx,
            pady=button_pady
        )
        self.button2.pack(side=LEFT)
        self.button2.bind("<Return>", self.button2Click_a)

        self.button3 = Button(self.button_frame, command=self.button3Click)
        self.button3.configure(text="Reset", background="red")
        self.button3.configure(
            width=button_width,
            padx=button_padx,
            pady=button_pady
        )

        self.button3.pack(side=LEFT, fill=X)
        self.button3.bind("<Return>", self.button3Click_a)

        # ---Status frame ---
        self.status_frame = Frame(self.myContainer1, borderwidth=5, background='grey')
        self.status_frame.pack(side=TOP, fill=X)

        myMessage = "Masking progress:\n"
        Label(self.status_frame, text=myMessage, justify=LEFT, background='grey').pack(side=TOP, anchor=W)

        self.progress = ttk.Progressbar(self.status_frame, length=300, mode='determinate')
        self.progress.pack(side=TOP, fill=X)

        # ---Coordinate frame ---
        self.coord_frame = Frame(self.myContainer1, borderwidth=5, background='grey')
        self.coord_frame.pack(expand=YES, fill=BOTH)

        myMessage = "Robot coordinates: \n"
        Label(self.coord_frame, text=myMessage, justify=LEFT, background='grey').pack(side=TOP, anchor=W)



    def button1Click(self):
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
            self.button1.configure(state="disabled")

    def button1Click_a(self, event):
        self.button1Click()

    def button2Click(self):
        if self.button1["background"] == "yellow":
            self.button1["background"] = "green"
            self.button1.configure(state="normal")

    def button2Click_a(self, event):
        self.button2Click()

    def button3Click(self):
        self.myParent.destroy()

    def button3Click_a(self, event):
        self.button3Click()


root = Tk()
root.title("Masking robot")
myapp = MyApp(root)
root.mainloop()
