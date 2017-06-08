from tkinter import *

import os
from _datetime import datetime
#from winsound import *
import threading
import time
import matplotlib
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import random

#This will adjust our graphs style as well as initilize our window
style.use('ggplot')
f =Figure(figsize=(4.8, 5), dpi=100)
a = f.add_subplot(111)

#This function grabs the data from the selected file
def animate(i):
    graph_data = open('trial.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(x)
            ys.append(y)
    a.clear()
    a.plot(ys)  #This plots just the y axis and x is set to the 1,2,3,4,5...

#This is the maine window which all code is within including graph
class Window_1(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.spacer = Label(self, text="", bg="light gray", fg="black", pady=10000, padx=100000, bd=5)
        self.spacer.pack({"side": "bottom"})

        self.initialize()
        self.main_labels()
        self.graph()
        self.binds()
        self.spinner()

    def initialize(self):
        self.two_comb = Label(self, text="", bg="light gray", fg="light gray", pady=290, padx=333, bd=5,font=("Courier", 12),borderwidth=5, relief="ridge")
        self.status = Label(self, text="", bg="gainsboro", fg="light gray", pady=90, padx=165, bd=5, font=("Courier", 12),borderwidth=3, relief="groove")
        self.readings = Label(self, text="", bg="gainsboro", fg="gray", pady=90, padx=125, bd=5, font=("Courier", 12),borderwidth=3, relief="groove")
        self.instructions = Label(self, text="", bg="gainsboro", fg="misty rose", pady=175, padx=165, bd=5, font=("Courier", 12),borderwidth=3, relief="groove")
        self.spinner_border = Label(self, text="", bg="gainsboro", fg="misty rose", pady=12, padx=125, bd=5,font=("Courier", 12),borderwidth=3, relief="groove")
        self.graph_border = Label(self, text="", bg="light gray", fg="light gray", pady=290, padx=265, bd=5,font=("Courier", 12),borderwidth=5, relief="ridge")

        self.batch_label = Label(self, text="Batch: closed ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.motor_label = Label(self, text="Motor: off  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")

        self.graph_label = Label(self, text="Graph of RPM", bg="dodger blue", fg="white", pady=10, padx=10, bd=2,font=("Courier", 15), borderwidth=0, relief="solid")

        self.rpm_label = Label(self, text="RPM:             ", bg="dodger blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")
        self.rpm_text = Label(self, text="0", bg="dodger blue", fg="white",font=("Courier", 12), borderwidth=0)
        self.temp_label = Label(self, text="Temperature:     ", bg="dodger blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")
        self.temp_text = Label(self, text="0", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.time_label = Label(self, text="Time:            ", bg="dodger blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")
        self.time_text = Label(self, text="0", bg="dodger blue", fg="white", font=("Courier", 12),borderwidth=0)

        self.spin_error = Label(self, text="Apperatus is ready!  ", bg="green", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")

        self.two_comb.place(x=15, y=25)
        self.status.place(x=25, y=35)
        self.readings.place(x=380, y=35)
        self.instructions.place(x=25, y=250)
        self.spinner_border.place(x=380, y=390)
        self.graph_border.place(x=720, y=25)

        self.graph_label.place(x=915,y=565)

        self.rpm_label.place(x=410, y=60)
        self.rpm_text.place(x=470, y=70)
        self.temp_label.place(x=410, y=115)
        self.temp_text.place(x=550, y=127)
        self.time_label.place(x=410, y=172)
        self.time_text.place(x=480, y=182)

        self.batch_label.place(x=50, y=115)
        self.motor_label.place(x=50, y=60)
        self.spin_error.place(x=50, y=170)

    def motor_run_key(self,event):
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])

        self.motor_label = Label(self, text="Motor: on   ", bg="green4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.motor_label.place(x=50, y=60)

        self.motor_on_write()

    def motor_on_write(self):
        if self.spinner.get() == "65 RPM":
            file = open('command_log.txt', 'a')
            file.write('65 RPM test started at ')
            file.write(self.time_keep)
            file.write('\n')
            file.close()
            self.motor_on_label()

        elif self.spinner.get()=="100 RPM":
            file = open('command_log.txt', 'a')
            file.write('100 RPM test started at ')
            file.write(self.time_keep)
            file.write('\n')
            file.close()
            self.motor_on_label()

        elif self.spinner.get()=="120 RPM":
            file = open('command_log.txt', 'a')
            file.write('120 RPM test started at ')
            file.write(self.time_keep)
            file.write('\n')
            file.close()
            self.motor_on_label()

        else:
            self.spin_error = Label(self, text="Reset your spinbox!  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
            self.spin_error.place(x=50, y=170)

    #Darute hides here
    def motor_on_label(self):
        self.motor_label = Label(self, text="Motor: on   ", bg="green4", fg="white", pady=10, padx=10, bd=5, font=("Courier", 12), borderwidth=2, relief="sunken")
        self.motor_label.place(x=50, y=60)

    def batch_release_key(self,event):
        #self.playSound_batch_release()
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])

        self.batch_label.place_forget()

        self.batch_label = Label(self, text="Batch: open   ", bg="green4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.batch_label.place(x=50, y=115)

        self.batch_write()

    def batch_write(self):
        file = open('command_log.txt', 'a')
        file.write('The batch Has been released at ')
        file.write(self.time_keep)
        file.write('\n')
        file.close()

    def motor_power_key(self,event):

        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])
        self.motor_label.place_forget()

        self.motor_label = Label(self, text="Motor: off  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="raised")
        self.motor_label.place(x=50, y=60)

        self.power_kill_write()

    def power_kill_write(self):
        file = open('command_log.txt', 'a')
        file.write('Power to the motor has been killed at ')
        file.write(self.time_keep)
        file.write('\n')
        file.close()

    def reset_experiment(self,event):
        self.batch_label.place_forget()
        self.motor_label.place_forget()
        self.spin_error.place_forget()
        self.rpm_text.place_forget()
        self.temp_text.place_forget()
        self.time_text.place_forget()

        self.batch_label = Label(self, text="Batch: closed ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="raised")
        self.motor_label = Label(self, text="Motor: off  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="raised")

        self.rpm_text = Label(self, text="0  ", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.temp_text = Label(self, text="0  ", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.time_text = Label(self, text="0  ", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)

        self.spin_error = Label(self, text="Apperatus is ready!  ", bg="green", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")

        self.rpm_text.place(x=470, y=70)
        self.temp_text.place(x=550, y=127)
        self.time_text.place(x=480, y=182)

        self.batch_label.place(x=50, y=115)
        self.motor_label.place(x=50, y=60)
        self.spin_error.place(x=50, y=170)

    def graph(self):
        canvas=FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().place(x=750,y=50)

    #This function is for display purposes (NOT NEEDED FOR FINAL CODE)
    def rand_write(self,event):
        self.f=str(random.randint(0,130))

        self.rand_write_file()

        self.rpm_text.place_forget()
        self.temp_text.place_forget()
        self.time_text.place_forget()


        self.rpm_text = Label(self, text=self.f + "   ", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.temp_text = Label(self, text=self.f +"  ", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.time_text = Label(self, text=self.f +"   " , bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)

        self.rpm_text.place(x=470, y=70)
        self.temp_text.place(x=550, y=127)
        self.time_text.place(x=480, y=182)

    def rand_write_file(self):
        g = open('trial.txt', 'a')
        g.write(',')
        g.write(self.f)
        g.write('\n')
        g.close()

    def close(self,event):
        global root
        root.quit()

    def main_labels(self):
        self.rand_add = Label(self, text="Add Graph Data: a ", bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.motor_run = Label(self, text="RUN MOTOR: L_Shift",bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.batch = Label(self, text="BATCH RELEASE: R_Shift", bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.motor_stop = Label(self, text="KILL MOTOR POWER: Enter",bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.reset_exp = Label(self, text="New Experiment: Back_Space ",bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.QUIT = Label(self, text="END EXPERIMENT: Escape", bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")



        self.motor_run.place(x=50,y=275)
        self.batch.place(x=50,y=330)
        self.motor_stop.place(x=50,y=385)
        self.reset_exp.place(x=50,y=440)
        self.QUIT.place(x=50,y=495)
        self.rand_add.place(x=50,y=550)

    def spinner(self):
        self.spinner = Spinbox(self, values=("65 RPM", "100 RPM", "120 RPM"), bd=5, width=28, wrap=True, relief="groove")
        self.spinner.place(x=410, y=400)

    def binds(self):
        root.bind('<a>', self.rand_write)
        root.bind('<Shift_L>', self.motor_run_key)
        root.bind('<Shift_R>', self.batch_release_key)
        root.bind('<Return>', self.motor_power_key)
        root.bind('<BackSpace>', self.reset_experiment)
        root.bind('<Escape>',self.close)

root = Tk()
app = Window_1(master=root)
#root.configure(background='red')
root.geometry("1400x700")
ani=animation.FuncAnimation(f,animate,interval=50)
app.mainloop()
root.destroy()

###########################List of things to possibly do:############################################
#Implement it so that commands are logged into a text file rather than displayed on the interface

#Add button to reset experiment. This button should reset all label status's to default as well as --
#-- write to a new file. This way data will be stored in new files for different experiments --
#-- This data should be written to a new file for the sensors, and command inputs



###########################List of things that need to be done:#######################################
#Make the graph scale properly
#Either make the music stop when new buttons are hit, or get rid of the music