import serial

import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

ser = serial.Serial('COM4', 115200, timeout = 0, parity = serial.PARITY_NONE)

#https://docs.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-6.0/aa299374(v=vs.60)
try:
    buf = []
    while(True):
        mes = (ser.read()).decode('utf-8')
        if mes:
            buf.append(mes)
        if len(buf) >= 2:

            command = buf[0] + buf[1]
            #mid button
            if command == 'sp':
                PressKey(0x1F)
            elif command == 'sr':
                ReleaseKey(0x1F)
                
            #top left button
            elif command == 'qp':
                PressKey(0x10)
            elif command == 'qr':
                ReleaseKey(0x10)

            #top right button
            elif command == 'ep':
                PressKey(0x12)
            elif command == 'er':
                ReleaseKey(0x12)

            #bottom left button
            elif command == 'zp':
                PressKey(0x2C)
            elif command == 'zr':
                ReleaseKey(0x2C)

            #bottom right button
            elif command == 'cp':
                PressKey(0x2E)
            elif command == 'cr':
                ReleaseKey(0x2E)

            else:
                print(command)
                pass
            buf = buf[2:]

finally:
    ser.close()
