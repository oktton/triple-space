from plyer import notification


def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=2,  # 持续时间（秒）
    )


def show_alert(title, message):
    # FIXME: not tested
    notification.notify(
        title=title,
        message=message,
        timeout=2,  # 持续时间（秒）
    )


if __name__ == "__main__":
    show_notification('123', '123')
