

from inputs import get_gamepad
import math
import threading
import numpy as np

class XboxController(object):

    ''' Class to read the inputs from an Xbox controller connected to the computer. '''
    ''' Automatically translates the inputs into the actions that the game expects. '''

    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.DPadX = 0
        self.DPadY = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.TopLeft = 0
        self.TopRight = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read_action(self): # return the buttons/triggers that you care about in this methode
        left_right = self.DPadX
        up_down = self.DPadY
        a = self.B
        b = self.A
        c = self.X
        done = self.Y
        save_checkpoint = self.TopRight

        if left_right == 1:
            action0 = 4
        elif left_right == -1:
            action0 = 3
        elif up_down == 1:
            action0 = 2
        elif up_down == -1:
            action0 = 1
        else:
            action0 = 0

        if a == 1:
            action1 = 1
        elif b == 1:
            action1 = 2
        elif c == 1:
            action1 = 3
        else:
            action1 = 0
        

        return np.array([action0, action1]), done == 1, save_checkpoint 

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'ABS_HAT0Y':
                    self.DPadY = event.state
                elif event.code == 'ABS_HAT0X':
                    self.DPadX = event.state
                elif event.code == 'BTN_TR':
                    self.TopRight = event.state
                elif event.code == 'BTN_TL':
                    self.TopLeft = event.state
                   
