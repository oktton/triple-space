import tkinter as tk
import unittest
import uuid

from native import clipboard_get, clipboard_set
from native import key_copy_all
from native import key_paste


def create_tk_input():
    root = tk.Tk()
    text_box = tk.Text(root)
    text_box.pack()
    root.attributes("-topmost", True)
    root.lift()

    root.iconify()
    root.deiconify()
    root.update_idletasks()
    text_box.focus_set()


    return root, text_box


def random_string():
    return uuid.uuid4().hex


class TestKeyboardPaste(unittest.TestCase):

    def test_copy_all(self):
        test_text = random_string()
        root, text_box = create_tk_input()

        text_box.insert(tk.END, test_text)

        root.after(300, key_copy_all)
        root.after(500, lambda: self.assertEqual(clipboard_get().strip(), test_text))
        root.after(900, lambda: (root.quit(), root.destroy()))
        root.mainloop()

    def test_key_paste(self):
        test_text = random_string()
        root, text_box = create_tk_input()

        clipboard_set(test_text)
        root.after(300, key_paste)
        root.after(500, lambda: self.assertEqual(text_box.get("1.0", "end-1c"), test_text))
        root.after(900, lambda: (root.quit(), root.destroy()))
        root.mainloop()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKeyboardPaste)
    runner = unittest.TextTestRunner()
    runner.run(suite)
