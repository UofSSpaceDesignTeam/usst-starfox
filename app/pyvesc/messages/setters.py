from pyvesc.messages.base import VESCMessage


class SetDutyCycle(metaclass=VESCMessage):
    """ Set the duty cycle.

    :ivar duty_cycle: Value of duty cycle to be set.
    """
    id = 5
    fields = [
        ('duty_cycle', 'i')
    ]


class SetRPM(metaclass=VESCMessage):
    """ Set the RPM.

    :ivar rpm: Value to set the RPM to.
    """
    id = 8
    fields = [
        ('rpm', 'i')
    ]


class SetCurrent(metaclass=VESCMessage):
    """ Set the current to the motor.

    :ivar current: Value to set the current to.
    """
    id = 6
    fields = [
        ('current', 'i')
    ]


class SetCurrentBrake(metaclass=VESCMessage):
    """ Set the current brake.

    :ivar current_brake: Value to set the current brake to.
    """
    id = 7
    fields = [
        ('current_brake', 'i')
    ]

class SetPosition(metaclass=VESCMessage):
    """
        Set the rotor angle based off of an encoder or sensor
        :ivar pos: Value to set the current position or angle to.
    """
    id = 9
    fields = [
        ('pos', 'i', 1000000)
    ]

class SetRotorPositionMode(metaclass=VESCMessage):
    """
        Sets the rotor position feedback mode.
        It is reccomended to use the defined modes as below
            DISP_POS_OFF
            DISP_POS_MODE_ENCODER
            DISP_POS_MODE_PID_POS
            DISP_POS_MODE_PID_POS_ERROR
        :ivar pos_mode: Value of the mode
    """

    DISP_POS_OFF = 0
    DISP_POS_MODE_ENCODER = 3
    DISP_POS_MODE_PID_POS = 4
    DISP_POS_MODE_PID_POS_ERROR = 5

    id = 10
    fields = [
        ('pos_mode', 'b')
    ]

class BatchRelease(metaclass=VESCMessage):
    """
        Sets the batch release signal.
        Internally controlled by firmware to be the correct duration.
    """

    id = 36
    fields = []
