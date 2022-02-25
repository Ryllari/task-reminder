def get_daily_reminders():
    with open("periodics/daily.txt", "r") as f:
        minute_reminders = f.readlines()
        return minute_reminders


def get_hour_reminders():
    with open("periodics/hour.txt", "r") as f:
        minute_reminders = f.readlines()
        return minute_reminders


def get_minute_reminders():
    with open("periodics/minute.txt", "r") as f:
        minute_reminders = f.readlines()
        return minute_reminders