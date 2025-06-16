import win32api
import win32con
import time

KEY_CTRL = win32con.VK_CONTROL
KEY_A = 0x41  # 'A'
KEY_C = 0x43  # 'C'
KEY_V = 0x56  # 'V'

def key_copy_all():
    win32api.keybd_event(KEY_CTRL, 0, 0, 0)
    win32api.keybd_event(KEY_A, 0, 0, 0)
    win32api.keybd_event(KEY_A, 0, win32con.KEYEVENTF_KEYUP, 0)

    win32api.keybd_event(KEY_C, 0, 0, 0)
    time.sleep(0.1)
    win32api.keybd_event(KEY_C, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(KEY_CTRL, 0, win32con.KEYEVENTF_KEYUP, 0)


def key_paste():
    win32api.keybd_event(KEY_CTRL, 0, 0, 0)
    win32api.keybd_event(KEY_V, 0, 0, 0)
    win32api.keybd_event(KEY_V, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(KEY_CTRL, 0, win32con.KEYEVENTF_KEYUP, 0)
