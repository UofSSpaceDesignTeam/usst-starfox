import threading
from Adafruit_BME280 import *
import time
import serial
from _datetime import datetime
from envirophat import motion
import pyvesc
from pyvesc import GetValues, SetRPM, SetCurrent, SetRotorPositionMode, GetRotorPosition, BatchRelease

from curses import wrapper as ncurses_wrapper
from curses_ui import ExperimentUI

class BME_280_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sensor = BME280(mode=BME280_OSAMPLE_8, address=0x76)
        self.degrees = 0
        self.humidity = 0
        self.kilopascals = 0
        self.quit = False
        print("BME280 thread ready!")

    def run(self):
        while not self.quit:
            self.degrees = self.sensor.read_temperature()
            pascals = self.sensor.read_pressure()
            self.kilopascals = pascals / 1000
            self.humidity = self.sensor.read_humidity()
            time.sleep(0.001)

    def return_values(self):
        return {"Temperature":self.degrees,"Pressure":self.kilopascals,"Humidity":self.humidity}

    def stop(self):
        self.quit = True

class LSMC_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.acc_val_dic = {"x":0,"y":0,"z":0}
        self.quit = False
        print("LSM thread ready!")

    def run(self):
        while not self.quit:
            acc_values = motion.accelerometer()
            self.acc_val_dic={"x":acc_values[0],"y":acc_values[1],"z":acc_values[2]}
            time.sleep(0.001)

    def return_accel_values(self):
        return self.acc_val_dic

    def stop(self):
        self.quit = True

class Motor_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0.05)
        self.rpm_set = 0
        self.rpm = 0
        self.tachometer=0
        self.watt_hours=0
        self.current_in=0
        self.quit = False
        print("Motor thread ready!")

    def set_rpm(self,rpm):
        try:
            self.rpm_set = rpm
        except:
            pass

    def batch_release(self):
        self.ser.write(pyvesc.encode(BatchRelease))

    def run(self):
        while not self.quit:
            self.ser.write(pyvesc.encode(SetRPM(self.rpm_set*12*19)))
            self.ser.write(pyvesc.encode_request(GetValues))

            # Check if there is enough data back for a measurement
            (response, consumed) = pyvesc.decode(self.ser.read(61))

            try:
                self.rpm=response.rpm
                self.tachometer=response.tachometer
                self.watt_hours=response.watt_hours
                self.current_in=response.current_in
            except:
                pass
            time.sleep(0.01)

    def return_motor_values(self):
        return {"RPM":self.rpm,"Tachometer":self.tachometer,"Watts":self.watt_hours,"Current":self.current_in}
       

    def stop(self):
        self.ser.write(pyvesc.encode(SetCurrent(0)))
        self.quit = True

BME_Thread = BME_280_Thread()
LSM_Thread = LSMC_Thread()
Motor_Thread = Motor_Thread()
UI_Thread = ncurses_wrapper(ExperimentUI, Motor_Thread)

def main():
    BME_Values=BME_Thread.return_values()
    Motor_values=Motor_Thread.return_motor_values()
    LSMC_values=LSM_Thread.return_accel_values()
    time_keep=(datetime.utcnow().strftime('%S.%f')[:-1])

    degrees=BME_Values["Temperature"]
    kilopascals=BME_Values["Pressure"]
    humidity=BME_Values["Humidity"]
    rpm=Motor_values["RPM"]
    tachometer=Motor_values["Tachometer"]
    watts=Motor_values["Watts"]
    current=Motor_values["Current"]
    x=LSMC_values["x"]
    y=LSMC_values["y"]
    z=LSMC_values["z"]


    to_save.write(str(time_keep))
    to_save.write(',       {0:3.3f},                {1:3.3f},               {2:3.3f},               {3:3.3f},               {4:3.3f},               {5:3.3f},               {6:3.3f},               {7:3.3f},               {8:3.3f},               {9:3.3f}                 '.format(degrees, kilopascals, humidity,x,y,z,rpm,tachometer,watts,current))
    to_save.write('\n')

    time.sleep(0.008)

path = '/home/starfox/log.csv'
to_save = open(path,'w')
to_save.write('Timestamp,     Temperature(C),        Pressure(KPA),        Humidity(Percent),          Accelearation(x y z),                                        RPM,          Tachometer,          Watts,          Current '+'\n')

try:
    BME_Thread.start()
    LSM_Thread.start()
    Motor_Thread.start()
    UI_Thread.start()

    while True:
        main()
        
except KeyboardInterrupt:
    BME_Thread.stop()
    LSM_Thread.stop()
    Motor_Thread.stop()
    UI_Thread.stop()
    quit()
