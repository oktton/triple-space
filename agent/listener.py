import time
from pynput import keyboard


class TripleSpacesListener():

    def __init__(self, on_fire):
        self.on_fire = on_fire
        self.space_count = 0
        self.last_press_time = 0
        self.kb_listener = keyboard.Listener(
            on_press=lambda key: self.on_press(key),
            on_release=lambda key: self.on_release(key))

    def on_press(self, key):
        print(f"on press, key = {key}")

        if key == keyboard.Key.space:
            self.space_count += 1

            time_to_last_press = time.time() - self.last_press_time
            print(self.space_count, time_to_last_press)

            if time_to_last_press > 0.2:
                self.space_count = 1
                self.last_press_time = time.time()
                return

            self.last_press_time = time.time()

            if self.space_count == 3:
                self.space_count = 0

                print("fire")
                self.on_fire()
                return

    def on_release(self, key):
        pass

    def __enter__(self):
        self.kb_listener.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kb_listener.stop()
