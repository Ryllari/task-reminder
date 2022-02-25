from celery import Celery
from celery.schedules import crontab
from plyer import notification


app = Celery('tasks', broker='redis://localhost:6379/0')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, send_minute_reminder.s(), name='Notify reminders every minute')
    sender.add_periodic_task(
        crontab(minute=0), 
        send_hour_reminder.s(),
        name='Notify reminders every hour'
    )
    sender.add_periodic_task(
        crontab(minute=0, hour=8), 
        send_hour_reminder.s(),
        name='Notify reminders daily at 8am'
    )


@app.task
def send_reminder(message):
    notification.notify(
        title='Você tem um lembrete!',
        message=message,
    )

# SCHEDULED REMINDERS
@app.task
def send_minute_reminder():
    from utils import get_minute_reminders
    for reminder in get_minute_reminders():
        notification.notify(
            title='Você tem um lembrete!',
            message=reminder,
        )


@app.task
def send_hour_reminder():
    from utils import get_hour_reminders
    for reminder in get_hour_reminders():
        notification.notify(
            title='Você tem um lembrete!',
            message=reminder,
        )


@app.task
def send_daily_reminder():
    from utils import get_daily_reminders
    for reminder in get_daily_reminders():
        notification.notify(
            title='Você tem um lembrete!',
            message=reminder,
        )
