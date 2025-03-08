from django_cron import CronJobBase, Schedule
from .utils import send_abandoned_cart_reminder  # Import the function above

class AbandonedCartReminderCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Run once per day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "main_app.abandoned_cart_reminder"

    def do(self):
        send_abandoned_cart_reminder()
