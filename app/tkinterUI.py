
from tkinter import *
import tkinter
import os
from _datetime import datetime
import threading
import time
import random
import sys



#Need to find a way for the batch timer to stop if we do manual power kill from motor or exp. test reset
#Need to add threading.Thread as a paramater for the class
class Window_1(Frame):

    def __init__(self, master=None, MotorThread=None):
        Frame.__init__(self, master)
        self.pack()
        
        self.root = master


        self.data_from_app = None

        self.MotorThread=MotorThread

    def starting(self):
        self.initialize()
        self.main_labels()
        self.binds()
       
        
            

    def initialize(self):
        self.spacer = Label(self, text="", bg="light gray", fg="black", pady=10000, padx=100000, bd=5)
        self.spacer.pack({"side": "bottom"})

        self.two_comb = Label(self, text="", bg="light gray", fg="light gray", pady=290, padx=310, bd=5,font=("Courier", 12),borderwidth=5, relief="ridge")
        self.status = Label(self, text="", bg="gainsboro", fg="light gray", pady=90, padx=165, bd=5, font=("Courier", 12),borderwidth=3, relief="groove")
        self.readings = Label(self, text="", bg="gainsboro", fg="gray", pady=90, padx=125, bd=5, font=("Courier", 12),borderwidth=3, relief="groove")
        self.instructions = Label(self, text="", bg="gainsboro", fg="misty rose", pady=175, padx=165, bd=5, font=("Courier", 12),borderwidth=3, relief="groove")
        self.test_border = Label(self, text="", bg="gainsboro", fg="misty rose", pady=175, padx=125, bd=5,font=("Courier", 12),borderwidth=3, relief="groove")

        self.rpm_label = Label(self, text="RPM:             ", bg="dodger blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")
        self.temp_label = Label(self,text="Acceleration:    ", bg="dodger blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")
        self.time_label = Label(self, text="Time:            ", bg="dodger blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")

        self.exp_status = Label(self, text="    Apperatus is ready!   ", bg="green", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")

        self.batch_time_on = Label(self, text= "Opened:          ", bg="dodger blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.batch_time_off = Label(self, text="Stop:            ", bg="dodger blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")

        self.batch_time_on.place(x=410, y=460)
        self.batch_time_off.place(x=410, y=515)

        self.tests_off()
        self.data_zero()
        self.status_off()

        self.two_comb.place(x=15, y=25)
        self.status.place(x=25, y=35)
        self.readings.place(x=373, y=35)
        self.instructions.place(x=25, y=250)
        self.test_border.place(x=373, y=250)

        self.rpm_label.place(x=410, y=60)
        self.temp_label.place(x=410, y=115)
        self.time_label.place(x=410, y=172)

        self.exp_status.place(x=50, y=170)

    def forget_data(self):
        self.rpm_text.place_forget()
        self.temp_text.place_forget()
        self.time_text.place_forget()

    def forget_test(self):
        self.test_1.place_forget()
        self.test_2.place_forget()
        self.test_3.place_forget()

    def forget_status(self):
        self.batch_label.place_forget()
        self.motor_label.place_forget()

    def tests_off(self):
        self.test_1 = Label(self, text="   68 RPM:  Off  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.test_2 = Label(self, text="   96 RPM: Off   ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.test_3 = Label(self, text="   118 RPM: Off  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")

        self.test_1.place(x=410, y=275)
        self.test_2.place(x=410, y=330)
        self.test_3.place(x=410, y=385)

    def status_off(self):
        self.batch_label = Label(self, text="      Batch: closed       ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.motor_label = Label(self, text="        Motor: off        ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.time_open = Label(self, text="        ", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.time_close = Label(self, text="        ", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)

        self.time_close.place(x=500, y=527)
        self.time_open.place(x=500, y=473)
        self.batch_label.place(x=50, y=115)
        self.motor_label.place(x=50, y=60)

    def data_zero(self):
        self.rpm_text = Label(self, text="0", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.temp_text = Label(self, text="0", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.time_text = Label(self, text="0", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)

        self.rpm_text.place(x=470, y=70)
        self.temp_text.place(x=550, y=127)
        self.time_text.place(x=480, y=182)

    def motor_run_key_1(self,event):
        self.test="68 RPM"

        self.MotorThread.set_rpm(68)

        self.forget_test()

        self.test_1 = Label(self, text="   68 RPM:  On   ", bg="green4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")
        self.test_2 = Label(self, text="   96 RPM: Off   ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.test_3 = Label(self, text="   118 RPM: Off  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")

        self.test_1.place(x=410, y=275)
        self.test_2.place(x=410, y=330)
        self.test_3.place(x=410, y=385)

        self.motor_on_write()

    def motor_run_key_2(self,event):
        self.test="96 RPM"

        self.MotorThread.set_rpm(96)

        self.forget_test()

        self.test_1 = Label(self, text="   68 RPM:  Off  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.test_2 = Label(self, text="   96 RPM: On    ", bg="green4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")
        self.test_3 = Label(self, text="   118 RPM: Off  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")

        self.test_1.place(x=410, y=275)
        self.test_2.place(x=410, y=330)
        self.test_3.place(x=410, y=385)
        self.motor_on_write()

    def motor_run_key_3(self,event):
        self.test="118 RPM"

        self.MotorThread.set_rpm(200)

        self.forget_test()

        self.test_1 = Label(self, text="   68 RPM:  Off  ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.test_2 = Label(self, text="   96 RPM: Off   ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")
        self.test_3 = Label(self, text="   118 RPM: On   ", bg="green4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="sunken")

        self.test_1.place(x=410, y=275)
        self.test_2.place(x=410, y=330)
        self.test_3.place(x=410, y=385)
        self.motor_on_write()

    def motor_on_write(self):
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])

        self.motor_label.place_forget()
        self.motor_label = Label(self, text="        Motor: on         ", bg="green4", fg="white", pady=10, padx=10,bd=5, font=("Courier", 12), borderwidth=2, relief="sunken")
        self.motor_label.place(x=50, y=60)

        if self.test == "68 RPM":
            file = open('command_log.txt', 'a')
            file.write('68 RPM test started at ')
            file.write(self.time_keep)
            file.write('\n')
            file.close()


        elif self.test=="96 RPM":
            file = open('command_log.txt', 'a')
            file.write('96 RPM test started at ')
            file.write(self.time_keep)
            file.write('\n')
            file.close()


        elif self.test=="118 RPM":
            file = open('command_log.txt', 'a')
            file.write('118 RPM test started at ')
            file.write(self.time_keep)
            file.write('\n')
            file.close()

    def batch_release_key(self,event):
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-7])
        self.batch_label.place_forget()

        self.MotorThread.batch_release()

        self.batch_label = Label(self, text="       Batch: open        ", bg="green4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="sunken")
        self.batch_label.place(x=50, y=115)

        self.time_open = Label(self, text=self.time_keep, bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.time_open.place(x=500, y=473)

        self.batch_write()

        
        timer = threading.Timer(20, self.stop_exper)
        timer.start()

    def stop_exper(self):
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-7])

        self.MotorThread.set_rpm(0)

        self.time_close = Label(self, text=self.time_keep, bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.motor_label = Label(self, text="        Motor: off        ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12), borderwidth=2, relief="raised")

        self.motor_label.place(x=50, y=60)
        self.time_close.place(x=500, y=527)

        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])
        file = open('command_log.txt', 'a')
        file.write('The experiment ended at ')
        file.write(self.time_keep)
        file.write('\n')
        file.close()

    def batch_write(self):
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])
        file = open('command_log.txt', 'a')
        file.write('The experiment started at ')
        file.write(self.time_keep)
        file.write('\n')
        file.close()

    def motor_power_key(self,event):
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-7])

        self.MotorThread.set_rpm(0)

        self.motor_label.place_forget()
        self.forget_test()
        self.tests_off()

        self.time_close = Label(self, text=self.time_keep, bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.time_close.place(x=500, y=527)

        self.motor_label = Label(self, text="        Motor: off        ", bg="red4", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="raised")
        self.motor_label.place(x=50, y=60)

        self.power_kill_write()

    def power_kill_write(self):
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])
        file = open('command_log.txt', 'a')
        file.write('Power to the motor has been killed at ')
        file.write(self.time_keep)
        file.write('\n')
        file.close()

    def reset_experiment(self,event):
        self.forget_status()
        self.forget_test()
        self.forget_data()
        self.tests_off()
        self.status_off()
        self.data_zero()

    def ui_showdata(self):

        if self.data_from_app is not None:
          
            data = self.data_from_app
            self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-4])

            self.forget_data()

            self.rpm_text = Label(self, text=(data["rpm"]), bg="dodger blue", fg="white", font=("Courier", 12),borderwidth=0)
            self.temp_text = Label(self, text=(data["acceleration"]), bg="dodger blue", fg="white", font=("Courier", 12),borderwidth=0)
            self.time_text = Label(self, text=(self.time_keep), bg="dodger blue", fg="white", font=("Courier", 12),borderwidth=0)

            self.rpm_text.place(x=470, y=70)
            self.temp_text.place(x=550, y=127)
            self.time_text.place(x=480, y=182)

    def rand_write(self,event):
        self.time_keep = (datetime.utcnow().strftime('%H.%M.%S.%f')[:-7])
        self.f=str(random.randint(0,130))

        self.forget_data()

        self.rpm_text = Label(self, text=self.f + "", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.temp_text = Label(self, text=self.f +"  ", bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)
        self.time_text = Label(self, text=self.time_keep , bg="dodger blue", fg="white", font=("Courier", 12), borderwidth=0)

        self.rpm_text.place(x=470, y=70)
        self.temp_text.place(x=550, y=127)
        self.time_text.place(x=480, y=182)

        self.rand_write_file()

    def rand_write_file(self):
        g = open('trial.txt', 'a')
        g.write(',')
        g.write(self.f)
        g.write('\n')
        g.close()

    def close(self,event):
        self.root.quit()   

    def main_labels(self):
        self.rand_add = Label(self,  text="     Add Graph Data: a     ", bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.motor_run = Label(self, text="RUN MOTOR:Tab,L_Shift,L_Alt",bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.batch = Label(self,     text="   BATCH RELEASE: R_Shift  ", bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.motor_stop = Label(self,text="  KILL MOTOR POWER: Enter  ",bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.reset_exp = Label(self, text=" New Experiment: Back_Space",bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")
        self.QUIT = Label(self,      text="   END EXPERIMENT: Escape  ", bg="midnight blue", fg="white", pady=10, padx=10, bd=5,font=("Courier", 12),borderwidth=2, relief="groove")



        self.motor_run.place(x=50,y=275)
        self.batch.place(x=50,y=330)
        self.motor_stop.place(x=50,y=385)
        self.reset_exp.place(x=50,y=440)
        self.QUIT.place(x=50,y=495)
        self.rand_add.place(x=50,y=550)

    def binds(self):
        self.root.bind('<a>', self.rand_write)
        self.root.bind('<F1>', self.motor_run_key_1)
        self.root.bind('<F2>', self.motor_run_key_2)
        self.root.bind('<F3>', self.motor_run_key_3)
        self.root.bind('<Shift_R>', self.batch_release_key)
        self.root.bind('<Return>', self.motor_power_key)
        self.root.bind('<BackSpace>', self.reset_experiment)
        self.root.bind('<Escape>',self.close)
        
class tkinter_starter():

    def __init__(self, MotorThread=None):
        self.MotorThread=MotorThread
        self.root = Tk()
        self.root.geometry("670x650")
        print("in loop")
        self.app = Window_1(master=self.root, MotorThread=self.MotorThread)
          
        
    def stop(self):
        self.root.destroy()
               
        
if __name__ == "__main__":
    ui_instance = tkinter_starter()

    try:
        ui_instance.start()
    except KeyboardInterrupt:
        ui_instance.stop()
        
###########################List of things to possibly do:############################################
#Add button to reset experiment. This button should reset all label status's to default as well as --
#-- write to a new file. This way data will be stored in new files for different experiments --
#-- This data should be written to a new file for the sensors, and command inputs

