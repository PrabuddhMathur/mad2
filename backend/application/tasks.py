from application.workers import celery
from celery.schedules import crontab
# from flask import render_template
from flask import current_app as app
from jinja2 import Template
from application.data_access import *
from application.models import *
from application.utils import *
import csv

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_month='1', hour=7, minute=30), 
        export_csv.s(), 
        name='add every month'
    )
    sender.add_periodic_task(
        crontab(hour=7),
        send_daily_reminders.s(),
        name="Daily Reminder"
        
    )

# @celery.task()
# def helloWorld():
#     print('Hello World!')
#     return "Hello World!"

@celery.task()
def export_csv():
    all_venues=get_all_venues()
    # all_shows=get_all_shows()

    with open("venue_analytics.csv", "w", newline='') as f:
        f = csv.writer(f, delimiter=',')
        f.writerow(["Venue ID","Venue Name","Venue Place","Venue Location","Venue Capacity"])
        for venue in all_venues:
            f.writerow([venue['venue_id'], venue['venue_name'],venue['venue_place'], venue['venue_location'],venue['venue_capacity']])

    template_str = """
        <p>
            Dear Admin,
        </p>
        <br />
        <p>
            As requested, we have attached your venue details analytics CSV file to this email. Please find it attached.
        </p>
        <p>
            If you have any questions or concerns about your analytics data, please don’t hesitate to reach out to us.
        </p>
        <br />
        <p>
            Best regards,
        </p>
        <p>
            Very Good Ticket Booking Site
        </p>
        """
    template = Template(template_str)

    address = "admin@admin.com"
    subject = "Venue Details Analytics CSV"
    message = template.render()

    file = open("venue_analytics.csv", "rb")

    send_email(address, subject, message, attachment=file, filename="venue_analytics.csv", subtype="csv")

    os.remove("venue_analytics.csv")

@celery.task()
def send_booking_mail(showname,username,total,email):
    template_str = """
        <p>
            Dear {{ username }},
        </p>
        <br />
        <p>
            Your tickets are confirmed for the show {{ showname }}. 
            Total tickets booked : {{ total }}
        </p>
        <p>
            If you have any questions or queries on this booking, please feel free to reply to this email. 
        </p>
        <br />
        <p>
            Happy binging,
        </p>
        <p>
            Very Good Ticket Booking Site
        </p>
        """
    template = Template(template_str)

    address = email
    subject = f"Booking Confirmed for {showname}!"
    message = template.render(username=username,showname=showname,total=total)

    send_email(address,subject,message)

@celery.task()
def send_daily_reminders():
    template_str = """
        <p>
            Hey {{ username }}!
        </p>
        <br />
        <p>
            It looks like you haven't visited in a while. Explore our new daily hits! 
        </p>
        <br />
        <p>
            Looking forward to see you there,
        </p>
        <p>
            Very Good Ticket Booking Site
        </p>
        """
    for user in get_status_users():
        if user.username!='admin':
            template = Template(template_str)
            address = user.email
            subject = f"Daily Reminder: Hey {user.username}! Check out our daily hits!"
            message = template.render(username=user.username)

            send_email(address,subject,message)
            
            get_status(user.id).visited=False
            db.session.commit()
    