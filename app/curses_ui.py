# Scatters dots randomly on your terminal as a quick demo of curses.

import curses
from curses import wrapper as ncurses_wrapper
import random
import time
import math
import threading
from _datetime import datetime


 

class ExperimentUI(threading.Thread):

    def __init__(self, stdscr, MotorThread=None):
        threading.Thread.__init__(self)
        self.experiment_name_list = ['68RPM Test', '96RPM Test', '118RPM Test', '200RPM Test']
        self.experiment_index = 0
        self.width = 0
        self.height = 0
        self.x_pos = 0
        self.quit = False
        self.time_keep=(datetime.utcnow().strftime('%M.%S.%f')[:-1])

        self.MotorThread = MotorThread

        self.window = stdscr

    def ui_showexperiment(self, dir):
        self.test1={"name":'68RPM Test',"rpm":68,"time":3}
        self.test2={"name":'96RPM Test',"rpm":96,"time":20}
        self.test3={"name":'118RPM Test',"rpm":118,"time":20}
        self.test4={"name":'200RPM Test',"rpm":200,"time":20}
        all_tests=[self.test1,self.test2,self.test3,self.test4]

        if(dir=='up'):
            self.experiment_index = self.experiment_index + 1

        elif(dir=='down'):
            self.experiment_index = self.experiment_index - 1

        elif(dir=='space'):
            self.window.addstr(10,5, "RUNNING             ")

            for i in all_tests:
                if i["name"]==self.experiment_name_list[self.experiment_index]:
                    self.MotorThread.set_rpm(i["rpm"])

        elif(dir=='right'):
            self.window.addstr(26,5, "BATCH RELEASED AT {}".format(datetime.utcnow().strftime('%M.%S.%f')[:-1]))
            self.window.addstr(10,5, "BATCH RELEASE         ")
            

            for i in all_tests:
                if i["name"]==self.experiment_name_list[self.experiment_index]:
                    self.MotorThread.batch_release()
                    timer=threading.Timer(i["time"], self.stop_motor)
                    timer.start()
                    

        elif(dir=='anything'):
            self.window.addstr(10,5, "STOP               ")
            self.MotorThread.set_rpm(0)


        if(self.experiment_index < 0):
            self.experiment_index = 0
        if(self.experiment_index > 3):
            self.experiment_index = 3

        name = self.experiment_name_list[self.experiment_index]
        self.window.addstr(12,5, "Selected Experiment: {}".format(name))

    def ui_showgraph(self, yval):

        self.x_pos = self.x_pos + 1
        if(self.x_pos >= self.width):
            self.x_pos = 0

        if(yval >= self.height):
            yval = self.height
        elif(yval <= 0):
            yval = 0

        self.window.addch(yval, self.x_pos, "*")

    def stop_motor(self):
        self.MotorThread.set_rpm(0)
        self.batch_timer()
        
    def batch_timer(self):
        self.batch_time=self.window.addstr(27,5, "TEST ENDED AT {}".format(datetime.utcnow().strftime('%M.%S.%f')[:-1]))

    def ui_showdata(self, data):
        
        self.window.addstr(14, 5, "RPM: {:1.4f}".format(data["rpm"]))
        self.window.addstr(15, 5, "Acceleration: {:1.4f}".format(data["acceleration"]))
        self.window.addstr(16, 5, "Temperature: {:1.4f}".format(data["Temperature"]))
        self.window.addstr(17, 5, "Humidity: {:1.4f}".format(data["Humidity"]))
        self.window.addstr(18, 5, "Pressure: {:1.4f}".format(data["Pressure"]))
        self.window.addstr(19, 5, "Time:")
        self.window.addstr(19, 11, (datetime.utcnow().strftime('%M.%S.%f')[:-1]))
        
    def stop(self):
        curses.nocbreak()
        self.window.keypad(0)
        curses.echo()
        curses.endwin()
        self.quit = True

    def run(self):

        self.window.clear()
        self.window.nodelay(True)
        curses.noecho()
        curses.cbreak()
        self.window.keypad(True)


        (self.height, self.width) = self.window.getmaxyx()

        self.window.addstr(10,5,'Idle')
        self.ui_showexperiment('none')
        self.window.addstr(21, 5, "CONTROLS:")
        self.window.addstr(22, 5, "space to start RPM")
        self.window.addstr(23, 5, "right arrow to release batch:")
        self.window.addstr(24, 5, "any button to stop rpm")

        while not self.quit:

            y = int(3 * math.cos((self.x_pos/12.0) * math.pi) + 5)

            self.ui_showgraph(y)

            key=self.window.getch()
            if(key == curses.KEY_UP):
                self.ui_showexperiment('up')
            elif(key == curses.KEY_DOWN):
                self.ui_showexperiment('down')
            elif(key == ord(' ')):
                self.ui_showexperiment('space')
            elif(key == curses.KEY_RIGHT):
                self.ui_showexperiment('right')
            elif(key != curses.ERR):
                self.ui_showexperiment('anything')


            self.window.refresh()
            time.sleep(0.05)

if __name__ == '__main__':
    try:
        ui = ncurses_wrapper(ExperimentUI)
        ui.start()
    except KeyboardInterrupt:
        print('Exiting')
        exit()
