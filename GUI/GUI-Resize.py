import tkinter.ttk as ttk
from tkinter import *
from tkinter.font import Font

from PIL import Image, ImageTk


class MyApp():
    def __init__(self, parent):
        # myrobot = MyRobot("192.168.1.102", 'COM3', False)
        # ---Font constants---
        mytitleFont = Font(family="Arial", size=16, weight="bold")
        mylabelFont = Font(family="Arial", size=14, weight="bold")
        mylabel_coordFont = Font(family="Arial", size=12)
        mybuttonFont = Font(family='Arial', size=12)

        img = Image.open('D:\Documents\SMR2\klm-embleme.jpg')
        img = img.resize((160, 100), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(img)

        self.myParent = parent

        self.myParent.attributes('-fullscreen', True)
        self.myParent.title("Masking Robot KLM")
        self.myParent['bg'] = '#00A1E4'
        self.myParent.grid_columnconfigure(0, weight=1)
        self.myParent.grid_rowconfigure(0, weight=1)
        self.myParent.grid_rowconfigure(1, weight=1)
        self.myParent.grid_rowconfigure(2, weight=1)
        self.myParent.grid_rowconfigure(3, weight=1)

        self.logo_frame = Frame(self.myParent, bg='#00A1E4')
        self.logo_frame.grid(row=0, column=0, sticky=NSEW)

        self.button_frame = Frame(self.myParent, bg='#00A1E4')
        self.button_frame.grid(row=1, column=0, sticky=NSEW)

        self.progress_frame = Frame(self.myParent, bg='#00A1E4')
        self.progress_frame.grid(row=2, column=0, sticky=NSEW)

        self.coord_frame = Frame(self.myParent, bg='#00A1E4')
        self.coord_frame.grid(row=3, column=0, sticky=NSEW)

        self.footer_frame = Frame(self.myParent, bg='#00A1E4')
        self.footer_frame.grid(row=4, column=0, sticky=NSEW)

        self.logo_frame.grid_rowconfigure(0, weight=1)
        self.logo_frame.grid_columnconfigure(0, weight=1)
        self.logo_frame.grid_columnconfigure(1, weight=1)

        self.button_frame.grid_rowconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)

        # self.progress_frame.grid_rowconfigure(2, weight=1)
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.coord_frame.grid_rowconfigure(3, weight=1)
        self.coord_frame.grid_rowconfigure(4, weight=1)
        self.coord_frame.grid_rowconfigure(5, weight=1)
        self.coord_frame.grid_columnconfigure(0, weight=1)
        self.coord_frame.grid_columnconfigure(1, weight=1)
        self.coord_frame.grid_columnconfigure(2, weight=1)
        self.coord_frame.grid_columnconfigure(3, weight=1)
        self.coord_frame.grid_columnconfigure(4, weight=1)
        self.coord_frame.grid_columnconfigure(5, weight=1)

        # self.footer_frame.grid_rowconfigure(6, weight=1)
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.head_label = Label(self.logo_frame, text='KLM TAPE MASKING ROBOT', padx=25, pady=25)
        self.head_label.configure(font=mytitleFont, bg='#00A1E4', foreground='white')
        self.head_label.grid(row=0, column=0, sticky='EWNS')

        self.logo_label = Label(self.logo_frame, image=logo, bg='#00A1E4')
        self.logo_label.image = logo
        self.logo_label.grid(row=0, column=1, sticky='EWNS')

        self.start_button = Button(self.button_frame, command=self.button_start_click, padx=5, pady=5, text='Start')
        self.start_button.configure(font=mybuttonFont, relief=RAISED)
        self.start_button.grid(row=0, column=0, pady=25, padx=25, sticky='EWNS')
        self.start_button.bind("<Return>", self.button_start_click_a)

        self.stop_button = Button(self.button_frame, command=self.button_stop_click, padx=5, pady=5, text='Stop')
        self.stop_button.configure(font=mybuttonFont, relief=RAISED)
        self.stop_button.grid(row=0, column=1, pady=25, padx=25, sticky='EWNS')
        self.stop_button.bind("<Return>", self.button_stop_click_a)

        self.reset_button = Button(self.button_frame, padx=5, pady=5, text='Reset')
        self.reset_button.configure(font=mybuttonFont, relief=RAISED)
        self.reset_button.grid(row=0, column=2, pady=25, padx=25, sticky='EWNS')

        self.exit_button = Button(self.button_frame, command=self.button_exit_click, padx=5, pady=5, text='Exit')
        self.exit_button.configure(font=mybuttonFont, relief=RAISED)
        self.exit_button.grid(row=0, column=3, pady=25, padx=25, sticky='EWNS')
        self.exit_button.bind("<Return>", self.button_exit_click_a)

        self.progress = ttk.Progressbar(self.progress_frame, mode='determinate', length=300)
        self.progress.grid(column=0, row=2, padx=5, pady=25, sticky='EWNS')

        mylabel_text = ['X', 'Y', 'Z', 'RX', 'RY', 'RZ']

        for row_index, text in enumerate(mylabel_text):
            if row_index < (len(mylabel_text) / 2):
                mylabels = Label(self.coord_frame, text=text)
                mylabels.configure(font=mylabelFont, bg='#00A1E4', foreground='white')
                mylabels.grid(column=0, row=row_index, sticky='EWNS', padx=5, pady=15)
            else:
                mylabels = Label(self.coord_frame, text=text)
                mylabels.configure(font=mylabelFont, bg='#00A1E4', foreground='white')
                mylabels.grid(column=3, row=row_index-3, sticky='EWNS', padx=5, pady=15)

        mycoords = ['5.55', '6.66', '7.77', '8.88', '9.99', '1.11']

        for row_index, text in enumerate(mycoords):
            if row_index < (len(mycoords) / 2):
                mylabels = Label(self.coord_frame, text=text)
                mylabels.configure(font=mylabel_coordFont, bg='white', relief=SUNKEN)
                mylabels.grid(column=1, row=row_index, sticky='EWNS')
            else:
                mylabels = Label(self.coord_frame, text=text)
                mylabels.configure(font=mylabel_coordFont, bg='white', relief=SUNKEN)
                mylabels.grid(column=4, row=row_index - 3, sticky='EWNS')

        Label(self.footer_frame, text="", pady=20, background="#00A1E4").grid(column=0, row=0, sticky='EWNS')

    def button_start_click(self):
        self.start_button.configure(state="disabled")

    def button_start_click_a(self):
        self.button_start_click()

    def button_stop_click(self):
        self.start_button.configure(state="normal")

    def button_stop_click_a(self):
        self.button_stop_click()

    def button_exit_click(self):
        root.destroy()

    def button_exit_click_a(self, event):
        self.button_exit_click()


root = Tk()
myapp = MyApp(root)  # , "192.168.1.102", 'COM3', False)
root.mainloop()
