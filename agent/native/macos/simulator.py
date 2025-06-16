from Quartz.CoreGraphics import (
    CGEventCreateKeyboardEvent,
    CGEventPost,
    CGEventSetFlags,
    kCGEventFlagMaskCommand,
    kCGHIDEventTap
)

KEY_A = 0x00
KEY_C = 0x08
KEY_V = 0x09


def key_event(keycode, keydown=True, with_command=False):
    event = CGEventCreateKeyboardEvent(None, keycode, keydown)
    if with_command:
        CGEventSetFlags(event, kCGEventFlagMaskCommand)  # 设置 Command 键
    CGEventPost(kCGHIDEventTap, event)


def key_copy_all():
    key_event(KEY_A, True, with_command=True)  # 'A' Down with Command
    key_event(KEY_A, False, with_command=True)  # 'A' Up with Command

    key_event(KEY_C, True, with_command=True)  # 'C' Down with Command
    key_event(KEY_C, False, with_command=True)  # 'C' Up with Command


def key_paste():
    key_event(KEY_V, True, with_command=True)  # 'V' Down with Command
    key_event(KEY_V, False, with_command=True)  # 'V' Up with Command
