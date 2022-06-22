from .models import Task
from django.contrib.auth.models import User
from datetime import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = os.getenv('user')
    msg['from'] = user
    password = os.getenv('pass')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()


def my_job():
    tasks = Task.objects.filter(status='Pending')
    if len(tasks) > 0:
        for task in tasks:
            today = datetime.today().strftime('%Y-%m-%d')
            task_date = task.date.strftime('%Y-%m-%d')
            time = (datetime.now()).strftime("%H:%M:%S")
            if task_date < today:
                task.status = 'Due'
                task.save()
            elif task_date == today and task.time.strftime("%H:%M:%S") < time:
                task.status = 'Due'
                task.save()
            elif task_date == today:
                user = User.objects.get(username=task.user)
                body = 'Hello User!\n\nThis is to remind you regaring your task ' + \
                    task.task_name+'.'
                email_alert('RemindX Remainder', task.task_name, user.email)


# if __name__ == '__main__':
#     email_alert('Alert Message', 'Hello World!', 'williamsparre@gmail.com')
