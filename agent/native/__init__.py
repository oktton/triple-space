import sys

__all__ = [
    "key_paste",
    "key_copy_all",
    "clipboard_get",
    "clipboard_set",
    "show_notification",
    "show_alert"
]

if sys.platform == "darwin":
    from .macos.simulator import key_paste, key_copy_all
    from .macos.clipboards import clipboard_get, clipboard_set
    from .macos.notification import show_notification, show_alert
elif sys.platform == "win32":
    from .windows.simulator import key_paste, key_copy_all
    from .windows.clipboards import clipboard_get, clipboard_set
    from .windows.notification import show_notification, show_alert
