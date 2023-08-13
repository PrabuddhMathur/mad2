from application.workers import celery
from celery.schedules import crontab
from flask import render_template
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
        monthly_report.s(), 
        name='Monthly Analytics Report'
    )
    sender.add_periodic_task(
        crontab(hour=7),
        send_daily_reminders.s(),
        name="Daily Reminder"
    )

@celery.task
def monthly_report():
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "support@verygoodmoviebookingsite.com"
    SENDER_PASSWORD = ""
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = "admin@admin.com"
    msg["Subject"] = "Admin Monthly Report"
    template = render_template("monthly_report.html")
    msg.attach(MIMEText(template, "html"))

    images=['show_details.png','venue_details.png']
    for image in images:
        with open("static/" + image, "rb") as fp:
            img = MIMEImage(fp.read(), _subtype='png')
        img.add_header('Content-ID', '<{}>'.format(image))
        msg.attach(img)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

@celery.task()
def export_venue_csv(venue_id,user_id):
    the_venue=get_venue_by_id(venue_id)
    the_shows=get_shows_by_venue_id(venue_id)[0]
    user=get_user_by_id(user_id)

    with open("venue_analytics.csv", "w", newline='') as f:
        f = csv.writer(f, delimiter=',')
        f.writerow(["Venue ID","Venue Name","Venue Place","Venue Location","Venue Capacity"])
        f.writerow([the_venue.venue_id,the_venue.venue_name,the_venue.venue_place,the_venue.venue_location,the_venue.venue_capacity])
        f.writerow(["Show ID","Show Name","Show Genre","Show Timing","Ticket Price","Available Tickets","Rating"])
        for show in the_shows:
            show_venue=get_showvenue_by_show_id(show.show_id)
            f.writerow([show.show_id,show.show_name, show.show_tags,show.show_timing,show.show_ticketprice,show_venue.available_tickets,show.show_rating])
            f.writerow(["Booking ID","Tickets Booked"])
            bookings=get_bookings_by_show_id(show.show_id)
            for booking in bookings:
                f.writerow([booking.booking_id,booking.booking_tickets])

    template_str = """
        <p>
            Dear {{username}},
        </p>
        <br />
        <p>
            As requested, we have attached CSV report for {{ venue_name }} in this email.
        </p>
        <p>
            If you have any questions or concerns about the report, please don\'t hesitate to reach out to us.
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

    address = user.email
    subject = f"{the_venue.venue_name} details CSV Export"
    message = template.render(username=user.username,venue_name=the_venue.venue_name)

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
           We are missing you! It looks like you haven't visited in a while. Explore our new daily hits! 
        </p>
        <br />
        <p>
            Looking forward to see you there,
        </p>
        <p>
            Very Good Ticket Booking Site
        </p>
        """
    users=Visited.query.all()
    for user in users:
        if user.user_id!=1:
            if not user.status:
                template = Template(template_str)
                address = get_user_by_id(user.user_id).email
                subject = f"Daily Reminder: Hey {get_user_by_id(user.user_id).username}! Check out our daily hits!"
                message = template.render(username=get_user_by_id(user.user_id).username)

                send_email(address,subject,message)

            else:
                user.status=False
                db.session.commit()
