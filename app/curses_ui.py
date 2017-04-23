# Scatters dots randomly on your terminal as a quick demo of curses.

import curses
from curses import wrapper as ncurses_wrapper
import random
import time
import math
import threading


class ExperimentUI(threading.Thread):

    def __init__(self, stdscr, MotorThread=None):
        threading.Thread.__init__(self)
        self.experiment_name_list = ['Test 1', 'Test 2', 'Test 3', 'Test 4']
        self.experiment_index = 0
        self.width = 0
        self.height = 0
        self.x_pos = 0
        self.quit = False
        self.MotorThread = MotorThread

        self.window = stdscr

    def ui_showexperiment(self, dir):
        if(dir=='up'):
            self.experiment_index = self.experiment_index + 1
            
        elif(dir=='down'):
            self.experiment_index = self.experiment_index - 1
            
        elif(dir=='space'):
            self.window.addstr(10,5, "RUNNING             ")
            
            
        elif(dir=='anything'):
            self.window.addstr(10,5, "Stop         ")
            

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

    def ui_showdata(self, data):
        self.window.addstr(14, 5, "Data 1: {:1.9f}".format(data))
        self.window.addstr(15, 5, "Data 2: {:1.9f}".format(data))
        self.window.addstr(16, 5, "Data 3: {:1.9f}".format(data))

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
        
        #self.MotorThread.set_rpm(100)

        (self.height, self.width) = self.window.getmaxyx()

        self.window.addstr(10,5,'Idle')
        self.ui_showexperiment('none')

        while not self.quit:

            y = int(3 * math.cos((self.x_pos/12.0) * math.pi) + 5)

            self.ui_showgraph(y)
            self.ui_showdata(random.random())

            key=self.window.getch()
            if(key == curses.KEY_UP):
                self.ui_showexperiment('up')
            elif(key == curses.KEY_DOWN):
                self.ui_showexperiment('down')
            elif(key == ord(' ')):
                self.ui_showexperiment('space')
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
