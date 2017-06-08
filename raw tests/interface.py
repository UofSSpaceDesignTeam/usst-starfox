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
f = Figure(figsize=(5, 5), dpi=100)
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
        self.spinner()
        self.main_labels()
        self.binds()
        self.graph()

        self.batch_label = Label(self, text="Batch: closed ", bg="red", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.motor_label = Label(self, text="Motor: off  ", bg="red", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")

        self.rpm_label = Label(self, text="RPM: 0   ", bg="yellow", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.temp_label = Label(self, text="Temperature: 0   ", bg="red", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.time_label = Label(self, text="Time: 0   ", bg="green", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")

        self.spin_error = Label(self, text="Apperatus is ready!  ", bg="green", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")

        self.spin_error.place(x=0, y=580)

        self.rpm_label.place(x=0, y=380)
        self.temp_label.place(x=150, y=380)
        self.time_label.place(x=400, y=380)


        self.batch_label.place(x=0, y=480)
        self.motor_label.place(x=200, y=480)

    def motor_run_key(self,event):
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])

        self.motor_label = Label(self, text="Motor: on   ", bg="green", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.motor_label.place(x=200, y=480)

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
            self.spin_error = Label(self, text="Reset your spinbox!  ", bg="red", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")
            self.spin_error.place(x=0, y=580)

    #Darute hides here
    def motor_on_label(self):
        self.motor_label = Label(self, text="Motor: on   ", bg="green", fg="black", pady=10, padx=10, bd=5, font=("Courier", 12), borderwidth=2, relief="sunken")
        self.motor_label.place(x=200, y=480)

    def batch_release_key(self,event):
        #self.playSound_batch_release()
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])

        self.batch_label = Label(self, text="Batch: open   ", bg="green", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.batch_label.place(x=0, y=480)

        self.batch_write()

    def batch_write(self):
        file = open('command_log.txt', 'a')
        file.write('The batch Has been released at ')
        file.write(self.time_keep)
        file.write('\n')
        file.close()

    def motor_power_key(self,event):
        #self.playSound_motor_cut()
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])

        self.motor_label = Label(self, text="Motor: off  ", bg="red", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.motor_label.place(x=200, y=480)

        self.power_kill_write()

    def power_kill_write(self):
        file = open('command_log.txt', 'a')
        file.write('Power to the motor has been killed at ')
        file.write(self.time_keep)
        file.write('\n')
        file.close()

    def reset_experiment(self,event):
        #This function will reset all the labels and hopefully arrange it so that new text files are written to
        self.batch_label = Label(self, text="Batch: closed ", bg="red", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.motor_label = Label(self, text="Motor: off  ", bg="red", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")

        self.rpm_label = Label(self, text="RPM: 0    ", bg="yellow", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.temp_label = Label(self, text="Temperature: 0    ", bg="red", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.time_label = Label(self, text="Time: 0    ", bg="green", fg="black", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")

        self.spin_error = Label(self, text="Apperatus is ready!  ", bg="green", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")

        self.spin_error.place(x=0, y=580)

        self.rpm_label.place(x=0, y=380)
        self.temp_label.place(x=150, y=380)
        self.time_label.place(x=400, y=380)

        self.batch_label.place(x=0, y=480)
        self.motor_label.place(x=200, y=480)

    def graph(self):
        canvas=FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=False)

    #This function is for display purposes (NOT NEEDED FOR FINAL CODE)
    def rand_write(self,event):
        f=str(random.randint(0,130))
        g = open('trial.txt', 'a')
        g.write(',')
        g.write(f)
        g.write('\n')
        g.close()
        self.rpm_label = Label(self, text="RPM: "+f +"  ", bg="yellow", fg="black",pady=10,padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.temp_label = Label(self, text="Temperature: " + f +"  ", bg="red", fg="black",pady=10,padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.time_label = Label(self, text="Time: " + f +"  ", bg="green", fg="black",pady=10,padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")

        self.rpm_label.place(x=0,y=380)
        self.temp_label.place(x=150, y=380)
        self.time_label.place(x=400, y=380)

    def close(self,event):
        global root
        root.quit()

    def main_labels(self):
        self.rand_add = Label(self, text="Add Graph Data (a) ", bg="yellow", fg="black", pady=10, padx=10, bd=5)
        self.motor_run = Label(self, text="RUN MOTOR (L_Shift)", bg="green", fg="white", pady=20, padx=100000, bd=5)
        self.batch = Label(self, text="BATCH RELEASE (R_Shift)", bg="blue", fg="white", pady=20, padx=100000, bd=5)
        self.motor_stop = Label(self, text="KILL MOTOR POWER (Enter)", bg="orange", fg="black", pady=20, padx=100000,bd=5)
        self.reset_exp = Label(self, text="Reset Experiment (Back_Space) ", bg="black", fg="white", pady=20,padx=100000, bd=5)
        self.QUIT = Label(self, text="END EXPERIMENT (Escape)", bg="red", fg="black", pady=20, padx=100000,bd=5)
        self.spacer = Label(self, text="")
        self.spacer2 = Label(self, text="")

        self.motor_run.pack({"side": "top"})
        self.batch.pack({"side": "top"})
        self.motor_stop.pack({"side": "top"})
        self.reset_exp.pack({"side": "top"})
        self.QUIT.pack({"side": "top"})
        self.rand_add.pack({"side": "top"})
        self.spacer.pack({"side": "top"})
        self.spacer2.pack({"side": "top"})

    def spinner(self):
        self.spinner = Spinbox(self, values=("65 RPM", "100 RPM", "120 RPM"), bd=5, width=50)  # wrap=True)
        self.spinner.pack()

    def binds(self):
        root.bind('<a>', self.rand_write)
        root.bind('<Shift_L>', self.motor_run_key)
        root.bind('<Shift_R>', self.batch_release_key)
        root.bind('<Return>', self.motor_power_key)
        root.bind('<BackSpace>', self.reset_experiment)
        root.bind('<Escape>',self.close)

root = Tk()
app = Window_1(master=root)
root.geometry("1400x600")
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