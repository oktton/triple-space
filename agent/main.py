import time

import listener
from client import TextTransformer
from icon import run_tray_icon

from native import key_copy_all, key_paste
from native import clipboard_get, clipboard_set
from native import show_notification

def on_triple_spaces(texttransformer):
    text_pre = clipboard_get()
    key_copy_all()
    start_time = time.time()
    while True:
        text = clipboard_get()
        if text != text_pre:
            break
        elif time.time() - start_time > 5:
            break
    if len(text) > 200:
        return
    clipboard_set(texttransformer.transform(text))
    key_paste()


if __name__ == "__main__":
    transform_type = "translate"
    target_language = "en"
    api_url = "http://127.0.0.1:8000"
    texttransformer = TextTransformer(transform_type, target_language, api_url)
    with listener.TripleSpacesListener(on_fire=lambda: on_triple_spaces(texttransformer)):
        show_notification("Triple!", "Triple spaces listener started")
        run_tray_icon(texttransformer)
