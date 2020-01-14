import tkinter.ttk as ttk
from tkinter import *


class MyApp:
    def __init__(self, parent):
        self.myParent = parent

        self.myContainer1 = Frame(self.myParent)
        self.myContainer1.grid(row=0,column=0, sticky=NSEW)

        # ---Button constants---
        button_width = 6

        button_padx = "4m"
        button_pady = "1m"
        # --- end ---

        # ---Output Label---
        label_parent = self.myParent

        background = "white"

        # ---End---

        self.button1 = Button(self.myContainer1, command=self.button1Click)
        self.button1.configure(text="Start!", background="green")
        self.button1.configure(
            width=button_width,
            padx=button_padx,
            pady=button_pady
        )
        self.button1.bind("<Return>", self.button1Click_a)

        self.button2 = Button(self.myContainer1, command=self.button2Click)
        self.button2.configure(text="Stop!", background="red")
        self.button2.configure(
            width=button_width,
            padx=button_padx,
            pady=button_pady
        )
        self.button2.bind("<Return>", self.button2Click_a)

        self.button3 = Button(self.myContainer1, command=self.button3Click)
        self.button3.configure(text="Reset", background="red")
        self.button3.configure(
            width=button_width,
            padx=button_padx,
            pady=button_pady
        )
        self.button3.bind("<Return>", self.button3Click_a)


        self.button1.grid(column=0, columnspan=1, row=0, padx=5, pady=5, sticky=NSEW)
        self.button2.grid(column=1, columnspan=2, row=0, padx=5, pady=5, sticky=NSEW)
        self.button3.grid(column=3, columnspan=1, row=0, padx=5, pady=5, sticky=NSEW)

        self.progress = ttk.Progressbar(self.myContainer1, mode='determinate', length=300)
        self.progress.grid(column=0, columnspan=4, row=1, padx=5, pady=5, sticky="")

        Label(self.myContainer1, text="X").grid(column=0, row=2, sticky="", padx=5, pady=5)
        Label(self.myContainer1, text="Y").grid(column=0, row=3, sticky="", padx=5, pady=5)
        Label(self.myContainer1, text="Z").grid(column=0, row=4, sticky="", padx=5, pady=5)

        Label(self.myContainer1, text="RX").grid(column=2, row=2, sticky="", padx=5, pady=5)
        Label(self.myContainer1, text="RY").grid(column=2, row=3, sticky="", padx=5, pady=5)
        Label(self.myContainer1, text="RZ").grid(column=2, row=4, sticky="", padx=5, pady=5)

        myX = "5,55"
        myY = "6,66"
        myZ = "7,77"

        Label(self.myContainer1, text=myX, background="white", relief=SUNKEN, padx=20).grid(column=1, row=2, sticky="W")
        Label(self.myContainer1, text=myY, background="white", relief=SUNKEN, padx=20).grid(column=1, row=3, sticky="W")
        Label(self.myContainer1, text=myZ, background="white", relief=SUNKEN, padx=20).grid(column=1, row=4, sticky="W")

        myRX = "8,88"
        myRY = "9,99"
        myRZ = "1,11"
        Label(self.myContainer1, text=myRX, background="white", relief=SUNKEN, padx=20).grid(column=3, row=2, sticky="W")
        Label(self.myContainer1, text=myRY, background="white", relief=SUNKEN, padx=20).grid(column=3, row=3, sticky="W")
        Label(self.myContainer1, text=myRZ, background="white", relief=SUNKEN, padx=20).grid(column=3, row=4, sticky="W")

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
#root.attributes('-fullscreen', True)
myapp = MyApp(root)

root.mainloop()
