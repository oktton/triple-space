import unittest
import uuid

from native import clipboard_set, clipboard_get


def random_string():
    return uuid.uuid4().hex


class TestClipboard(unittest.TestCase):

    def test_clipboard_get_set(self):
        old_text = clipboard_get()
        text = random_string()
        clipboard_set(text)
        self.assertEqual(clipboard_get(), text)
        self.assertNotEqual(clipboard_get(), old_text)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
