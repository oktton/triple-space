import tkinter as tk
import threading
from tkinter import messagebox, ttk
from pystray import Icon, MenuItem, Menu
from PIL import Image
import os
import re

root = tk.Tk()
root.withdraw()

# UI 界面（点击托盘图标时打开）
def show_ui(icon, texttransformer):
    # 最小化时重新显示
    existing_window = None
    for w in root.winfo_children():
        if isinstance(w, tk.Toplevel) and not hasattr(w, 'is_popup'):
            existing_window = w
            break

    if existing_window:
        if not existing_window.winfo_viewable():
            existing_window.deiconify()
        existing_window.lift()
        return

    top = tk.Toplevel(root)
    top.title("Triple Spaces App")
    top.geometry("300x300")

    tk.Label(top, text="Transform Type", font=("Arial", 16)).pack(pady=5)
    options = ["translate", "polish"]
    selected_option = tk.StringVar(value=texttransformer.transform_type)
    combobox = ttk.Combobox(top, textvariable=selected_option, values=options, state="readonly")
    combobox.pack(pady=5)

    tk.Label(top, text="Target Language:").pack(pady=5)
    entry_lan = tk.Entry(top, width=25)
    entry_lan.insert(0, texttransformer.target_language)
    entry_lan.pack(pady=5)

    tk.Label(top, text="API url:").pack(pady=5)
    entry_url = tk.Entry(top, width=25)
    entry_url.insert(0, texttransformer.api_url)
    entry_url.pack(pady=5)

    tk.Button(top, text="Submit", command=lambda: modify_parameters(texttransformer, selected_option.get(),
                                                                     entry_lan.get(), entry_url.get())).pack(pady=5)
    tk.Button(top, text="Exit", command=lambda: exit_program(icon)).pack(pady=5)

def modify_parameters(texttransformer, transform_type, target_language, api_url):
    if transform_type not in ["polish", "translate"]:
        messagebox.showerror("Error", "Transform type must be 'polish' or 'translate'")
        return

    if not isinstance(target_language, str) or not target_language.strip():
        messagebox.showerror("Error", "Target language must be a non-empty string")
        return

    url_pattern = r'^(http[s]?:\/\/)?([\w.-]+\.[a-zA-Z]{2,}|(\d{1,3}\.){3}\d{1,3})(:\d+)?([\/\w\.-]*)*\/?$'
    if not re.match(url_pattern, api_url):
        messagebox.showerror("Error", "Invalid API URL format")
        return

    texttransformer.transform_type = transform_type
    texttransformer.target_language = target_language
    texttransformer.api_url = api_url

    messagebox.showinfo("Triple", "Parameters updated successfully!")

def exit_program(icon, item=None):
    root.quit()
    icon.stop()

def run_tray_icon(texttransformer=None):
    menu_exit = MenuItem("Exit", exit_program)
    left_click = MenuItem(text="Control Panel", action=lambda: show_ui(icon, texttransformer), default=True)
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', "icon.ico")
    icon = Icon("test_icon", Image.open(icon_path), "Triple Spaces", Menu(left_click, menu_exit))
    threading.Thread(target=icon.run, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    from client import TextTransformer
    transform_type = "translate"
    target_language = "en"
    api_url = "http://127.0.0.1:8000"
    texttransformer = TextTransformer(transform_type, target_language, api_url)
    run_tray_icon(TextTransformer)
