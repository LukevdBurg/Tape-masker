import tkinter.ttk as ttk
from tkinter import *


class MyApp:
    def __init__(self, parent):
        self.myParent = parent

        self.myParent.attributes('-fullscreen', True)
        self.myParent.title("Masking Robot KLM")
        self.myParent.grid_columnconfigure(0, weight=1)
        self.myParent.grid_rowconfigure(0, weight=1)

        self.button_frame = Frame(self.myParent, bg='grey')
        self.button_frame.grid(row=0, column=0, sticky=NSEW)

        self.progress_frame = Frame(self.myParent, bg='grey')
        self.progress_frame.grid(row=1, column=0, sticky=NSEW)

        self.coord_frame = Frame(self.myParent, bg='grey')
        self.coord_frame.grid(row=2, column=0, sticky=NSEW)

        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)

        self.progress_frame.grid_rowconfigure(1, weight=1)
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.coord_frame.grid_rowconfigure(2, weight=1)
        self.coord_frame.grid_rowconfigure(3, weight=1)
        self.coord_frame.grid_rowconfigure(4, weight=1)
        self.coord_frame.grid_columnconfigure(0, weight=1)
        self.coord_frame.grid_columnconfigure(1, weight=1)
        self.coord_frame.grid_columnconfigure(2, weight=1)
        self.coord_frame.grid_columnconfigure(3, weight=1)

        self.start_button = Button(self.button_frame, command=self.buttonstartclick, padx=5, pady=5, text='Start',
                                   background='green')
        self.start_button.grid(row=0, column=0, pady=25, padx=25, sticky='EWNS')
        self.start_button.bind("<Return>", self.buttonstartclick_a)

        self.stop_button = Button(self.button_frame, command=self.buttonstopclick, padx=5, pady=5, text='Stop',
                                  background='red')
        self.stop_button.grid(row=0, column=1, pady=25, padx=25, sticky='EWNS')
        self.stop_button.bind("<Return>", self.buttonstopclick_a)

        self.reset_button = Button(self.button_frame, padx=5, pady=5, text='Reset', background='red')
        self.reset_button.grid(row=0, column=2, pady=25, padx=25, sticky='EWNS')

        self.exit_button = Button(self.button_frame, command=self.buttonexitclick, padx=5, pady=5, text='Exit')
        self.exit_button.grid(row=0, column=3, pady=25, padx=25, sticky='EWNS')
        self.exit_button.bind("<Return>", self.buttonexitclick_a)

        self.progress = ttk.Progressbar(self.progress_frame, mode='determinate', length=300)
        self.progress.grid(column=0, columnspan=4, row=2, padx=5, pady=25, sticky='EWNS')

        Label(self.coord_frame, text="X", background='grey').grid(column=0, row=0, sticky='EWNS', padx=5, pady=15)
        Label(self.coord_frame, text="Y", background='grey').grid(column=0, row=1, sticky='EWNS', padx=5, pady=15)
        Label(self.coord_frame, text="Z", background='grey').grid(column=0, row=2, sticky='EWNS', padx=5, pady=15)

        Label(self.coord_frame, text="RX", background='grey').grid(column=2, row=0, sticky='EWNS', padx=5, pady=15)
        Label(self.coord_frame, text="RY", background='grey').grid(column=2, row=1, sticky='EWNS', padx=5, pady=15)
        Label(self.coord_frame, text="RZ", background='grey').grid(column=2, row=2, sticky='EWNS', padx=5, pady=15)

        myX = "5,55"
        myY = "6,66"
        myZ = "7,77"

        Label(self.coord_frame, text=myX, background="white", relief=SUNKEN, padx=20, pady=20).grid(column=1, row=0,
                                                                                                    sticky='EWNS')
        Label(self.coord_frame, text=myY, background="white", relief=SUNKEN, padx=20, pady=20).grid(column=1, row=1,
                                                                                                    sticky='EWNS')
        Label(self.coord_frame, text=myZ, background="white", relief=SUNKEN, padx=20, pady=20).grid(column=1, row=2,
                                                                                                    sticky='EWNS')

        myRX = "8,88"
        myRY = "9,99"
        myRZ = "1,11"

        Label(self.coord_frame, text=myRX, background="white", relief=SUNKEN, padx=20, pady=20).grid(column=3, row=0,
                                                                                                     sticky='EWNS')
        Label(self.coord_frame, text=myRY, background="white", relief=SUNKEN, padx=20, pady=20).grid(column=3, row=1,
                                                                                                     sticky='EWNS')
        Label(self.coord_frame, text=myRZ, background="white", relief=SUNKEN, padx=20, pady=20).grid(column=3, row=2,
                                                                                                     sticky='EWNS')

    def buttonstartclick(self):
        if self.start_button["background"] == 'green':
            self.start_button["background"] = "yellow"
            self.start_button.configure(state="disabled")

    def buttonstartclick_a(self):
        self.buttonstartclick()

    def buttonstopclick(self):
        if self.start_button["background"] == "yellow":
            self.start_button["background"] = "green"
            self.start_button.configure(state="normal")

    def buttonstopclick_a(self):
        self.buttonstopclick()

    def buttonexitclick(self):
        root.destroy()

    def buttonexitclick_a(self, event):
        self.buttonexitclick()


root = Tk()
myapp = MyApp(root)
root.mainloop()
