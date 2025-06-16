from native.windows.win_notify_api import notification


def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=2,  # 持续时间（秒）
        app_name="triple_spaces"
    )


def show_alert(title, message):
    # FIXME: not tested
    notification.notify(
        title=title,
        message=message,
        timeout=2,  # 持续时间（秒）
        app_name="triple_spaces"
    )


if __name__ == "__main__":

    from win_notify_api import notification
    show_notification('123', '123')