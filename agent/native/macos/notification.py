import subprocess


def show_alert(message):
    applescript = f'display alert "{message}"'
    subprocess.run(["osascript", "-e", applescript])


def show_notification(title, message):
    applescript = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", applescript])