import tkinter as tk
import win32gui
import threading
import time
import os
from icon import root  # 引入全局唯一tk对象
BASE_PATH = os.path.join(os.path.dirname(__file__), 'assets')

class LoadingPopup:
    def __init__(self):
        self.popup = None
        self.gif_label = None
        self.running = False
        self.status = "loading"
        self._create_window()
        while self.popup is None:  # 确保窗口初始化
            time.sleep(0.01)

    def update_status(self, status):
        self.status = status
        if self.popup:
            self._show_git()

    def _show_git(self):
        status = self.status
        gif_name = {
            "loading": "Loading_icon.gif",
            "sucess": "sucess_icon.gif",
            "erro": "erro_icon.gif"
        }.get(status)        
        gif_path = os.path.join(BASE_PATH, gif_name)
        self.frames = []
        i = 0
        while True:
            try:
                frame = tk.PhotoImage(file=gif_path, format=f'gif -index {i}')
                self.frames.append(frame)
                i += 1
            except:
                break
            
        # 给×和√延迟一点时间
        if status in ['erro', 'sucess']:
            last_frame = self.frames[-1]
            self.frames.extend([last_frame] * 100)

        def update_frame(idx=0):
            if not self.popup or self.status != status:
                return
            x, y = win32gui.GetCursorPos()
            self.popup.geometry(f"+{x+10}+{y+20}")
            self.gif_label.config(image=self.frames[idx])
            self.gif_label.image = self.frames[idx]
            if self.status != 'loading' and idx == len(self.frames) - 1:
                self.close_after(0)
                return
            self.popup.after(10, update_frame, (idx + 1) % len(self.frames))
        
        update_frame()

    def _create_window(self):
        self.popup = tk.Toplevel(root)
        self.popup.is_popup = True  # 用来标识是否是popup
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)
        self.popup.config(bg='white')
        self.popup.wm_attributes("-transparentcolor", "white")
        self.gif_label = tk.Label(self.popup, bg="white", bd=0, highlightthickness=0)
        self.gif_label.pack()

    def close_after(self, delay=1):
        def close():
            time.sleep(delay)
            if self.popup and self.popup.winfo_exists():
                self.popup.destroy()
        threading.Thread(target=close, daemon=False).start()

if __name__ == "__main__":
    popup = LoadingPopup()
    popup.update_status("loading")
    time.sleep(2)
    popup.update_status("sucess")
    popup.close_after(2)
