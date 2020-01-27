import socket
from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showerror

import urx
from PIL import Image, ImageTk

from Circle import MyRobot


class MyApp():
    def __init__(self, parent):

        # ---Font constants---
        mytitleFont = Font(family="Arial", size=16, weight="bold")
        mylabelFont = Font(family="Arial", size=14, weight="bold")
        mylabel_coordFont = Font(family="Arial", size=12)
        mybuttonFont = Font(family='Arial', size=12)

        img = Image.open('D:\Documents\Tape-masker\klm-embleme.jpg')
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

        self.coord_frame = Frame(self.myParent, bg='#00A1E4')
        self.coord_frame.grid(row=2, column=0, sticky=NSEW)

        self.footer_frame = Frame(self.myParent, bg='#00A1E4')
        self.footer_frame.grid(row=3, column=0, sticky=NSEW)

        self.demo_frame = Frame(self.myParent, bg='#00A1E4')
        self.demo_frame.grid(row=4, column=0, sticky=NSEW)

        # self.logo_frame.grid_rowconfigure(0, weight=1)
        self.logo_frame.grid_columnconfigure(0, weight=1)
        self.logo_frame.grid_columnconfigure(1, weight=1)

        # self.button_frame.grid_rowconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)

        self.coord_frame.grid_rowconfigure(0, weight=1)
        self.coord_frame.grid_rowconfigure(1, weight=1)
        self.coord_frame.grid_columnconfigure(0, weight=1)
        self.coord_frame.grid_columnconfigure(1, weight=1)
        self.coord_frame.grid_columnconfigure(2, weight=1)
        self.coord_frame.grid_columnconfigure(3, weight=1)

        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.demo_frame.grid_rowconfigure(0, weight=1)

        self.head_label = Label(self.logo_frame, text='KLM TAPE MASKING ROBOT', padx=25, pady=25)
        self.head_label.configure(font=mytitleFont, bg='#00A1E4', foreground='white')
        self.head_label.grid(row=0, column=0, padx=10, pady=10, sticky='EWNS')

        self.logo_label = Label(self.logo_frame, image=logo, bg='#00A1E4')
        self.logo_label.image = logo
        self.logo_label.grid(row=0, column=1, sticky='EWNS')

        mybuttons = ['Connect', 'Stop', 'Reset', 'Exit']
        self.buttons = []
        for column_index, button in enumerate(mybuttons):
            self.buttons.append(Button(self.button_frame, text=button,
                                       command=lambda column_index=column_index: self.button_click_a(column_index)))
            self.buttons[column_index].configure(font=mybuttonFont, relief=RAISED)
            self.buttons[column_index].grid(row=0, column=column_index, pady=25, padx=25, sticky='EWNS')

        mylabel_text = ['Connection with Robot: ', 'Connection with Lidar: ']

        for column_index, text in enumerate(mylabel_text):
            if column_index == 0:
                mylabels = Label(self.coord_frame, text=text)
                mylabels.configure(font=mylabelFont, bg='#00A1E4', foreground='white')
                mylabels.grid(column=column_index, row=0, sticky='EWNS', padx=5, pady=15)
            else:
                mylabels = Label(self.coord_frame, text=text)
                mylabels.configure(font=mylabelFont, bg='#00A1E4', foreground='white')
                mylabels.grid(column=column_index + 1, row=0, sticky='EWNS', padx=5, pady=15)

        self.mycoords = ['Not connected', 'Not connected']
        self.mylabels = []

        for column_index, text in enumerate(self.mycoords):
            if column_index == 0:
                self.mylabels.append(Label(self.coord_frame, text=text))
                self.mylabels[column_index].configure(font=mylabel_coordFont, bg='white', relief=SUNKEN)
                self.mylabels[column_index].grid(column=column_index + 1, row=0, padx=5, sticky='EWNS')
            else:
                self.mylabels.append(Label(self.coord_frame, text=text))
                self.mylabels[column_index].configure(font=mylabel_coordFont, bg='white', relief=SUNKEN)
                self.mylabels[column_index].grid(column=column_index + 2, row=0, padx=5, sticky='EWNS')

        self.console = Text(self.footer_frame, height=15)
        self.console.grid(column=0, row=0, pady=5, padx=25, sticky='EWNS')

        self.demo_state = IntVar()
        self.demo = Checkbutton(self.demo_frame, bg='#00A1E4', text='Demo',
                                variable=self.demo_state, onvalue=1, offvalue=0)
        self.demo.grid(column=1, row=0, pady=5, padx=25)

    def console_print(self, text):
        self.console.insert(END, text)

    def button_click_a(self, i):
        if i == 0:
            if self.buttons[0]["text"] == 'Start':
                self.console_print("Start button clicked \n")
            else:
                self.console_print("Start button clicked \n")
            self.button_start_click()
        elif i == 1:
            self.console_print("Stop button clicked \n")
            self.button_stop_click()
        elif i == 2:
            self.console_print("Reset button clicked \n")
            self.button_reset_click()
        elif i == 3:
            self.console_print("Exit button clicked \n")
            self.button_exit_click()

    def button_start_click(self):
        start_clicked = 0
        if self.buttons[0]["text"] == 'Start':
            start_clicked = 1

        if self.buttons[0]["text"] == 'Connect':
            try:
                self.myrobot = MyRobot("192.168.1.102", 'COM3')
            except socket.timeout as err:
                showerror("Socket error", "Could not connect with the robot\n Make sure the robot is plugged in!")
                self.console_print("Connection error, try again... \n")
            except socket.error as err:
                showerror("Socket error", "Could not connect with the robot\n Make sure the robot is plugged in!")
                self.console_print("Connection error, try again... \n")
            except urx.ursecmon.TimeoutException as err:
                showerror("Timeout error", "Could not connect with the robot\n Restart the robot!")
            else:
                self.buttons[0].configure(text='Start')

        if start_clicked == 1:
            self.buttons[0].configure(state='disabled')
            if self.demo_state == 1:
                self.console_print("Robot starting in Demo mode")
                self.myrobot.demo()
            else:
                self.console_print("Robot starting with masking \n")
                self.myrobot.run()

    def button_stop_click(self):
        # TODO stop the robot
        self.buttons[0].configure(state="normal")
        self.myrobot.stop()

    def button_reset_click(self):
        # TODO set everything back to begin state
        self.buttons[0].configure(state="normal")
        self.buttons[0].configure(text="Connect")
        self.myrobot.__del__()
        self.console_print("Back to begin state! \n")
        self.myrobot.mylidar.disconnect()

    def button_exit_click(self):
        self.console_print("Shutting down \n")
        root.destroy()


root = Tk()
myapp = MyApp(root)
root.mainloop()
