from flask import render_template, redirect,request,flash, url_for
from flask_security import login_required, current_user,roles_required
from .models import *
import html
from flask import current_app as app
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

@app.route("/api/venues")
def venues():
    venues=venue.query.all()
    return [venue.to_dict() for venue in venues]

@app.route("/api/shows")
def shows():
    shows=show.query.all()
    return [show.to_dict() for show in shows]

@app.route("/api/show_venues")
def show_venues():
    show_venues=show_venue.query.all()
    return [show_venue.to_dict() for show_venue in show_venues]

@app.route("/api/bookings")
def booking():
    show_bookings=bookings.query.all()
    return [show_booking.to_dict() for show_booking in show_bookings]



@app.route('/user_dashboard/search', methods=["GET"])
def search():
    venues=venue.query.all()
    shows=show.query.all()
    show_venues=show_venue.query.all()

    search_by_category=['Show','Venue','Location','Timing', 'Genre','Rating' ]

    search_value=request.args.get('search_value')
    search_query=request.args.get('search_query')
    query="%"+search_query+"%"
    
    available_locations=[ html.escape(i[0],quote=True) for i in db.session.query(venue.venue_location.distinct()).all()]
    available_genres=[ html.escape(i[0],quote=True) for i in db.session.query(show.show_tags.distinct()).all()]
    available_timings=[ html.escape(i[0],quote=True) for i in db.session.query(show.show_timing.distinct()).all()]
    available_shows=[ html.escape(i[0],quote=True) for i in db.session.query(show.show_name.distinct()).all()]
    available_venues=[ html.escape(i[0],quote=True) for i in db.session.query(venue.venue_name.distinct()).all()]

    if search_value=="Show":
        results=show.query.filter(show.show_name.like(query)).all()
    elif search_value=="Venue":
        results=venue.query.filter(venue.venue_name.like(query)).all()
    elif search_value=="Location":
        results=venue.query.filter(venue.venue_location.like(query)).all()
    elif search_value=="Timing":
        results=show.query.filter(show.show_timing.like(query)).all()
    elif search_value=="Genre":
        results=show.query.filter(show.show_tags.like(query)).all()
    elif search_value=="Rating":
        results=show.query.filter(show.show_rating.like(query)).all()
    
    return render_template('search.html', venues=venues, shows=shows, show_venues=show_venues,search_by_category=search_by_category,search_value=search_value,search_query=search_query,available_locations=available_locations,available_genres=available_genres,available_timings=available_timings,available_shows=available_shows,available_venues=available_venues,results=results)


@app.route("/admin_summary", methods=["GET", "POST"])
def admin_summary():
    show_venues=show_venue.query.all()
    x=[]
    y=[]
    for i in show_venues:
        show_details=show.query.filter_by(show_id=i.show_id).first()
        x.append(show_details.show_name)
        y.append(i.available_tickets)


    plt.bar(x,y, width=0.5)
    plt.xlabel('Show Name')
    plt.ylabel('Available Tickets')
    
    plt.savefig(f"./static/{current_user.id}_show_venue.png")
    plt.clf()

    venues=venue.query.all()
    x=[]
    y=[]
    for i in venues:
        venue_details=venue.query.filter_by(venue_id=i.venue_id).first()
        x.append(venue_details.venue_name)
        y.append(i.venue_capacity)

    print(x,y)
    plt.bar(x,y, width=0.5)
    plt.xlabel('Venue Name')
    plt.ylabel('Venue Capacity')
    
    plt.savefig(f"./static/{current_user.id}_venue.png")
    plt.clf()

    return render_template("admin_summary.html")

@app.route("/create/venue", methods=["POST"])
def create_venue():
    venue_name=request.form.get('venue')
    venue_place=request.form.get('place')
    venue_location=request.form.get('location')
    venue_capacity=request.form.get('capacity')

    from application.database import db
    new_venue=venue(venue_name=venue_name, venue_place=venue_place, venue_location=venue_location, venue_capacity=venue_capacity)

    db.session.add(new_venue)
    db.session.commit()

    return "Success",200

@app.route("/edit/venue/<int:venue_id>", methods=["POST"])
def edit_venue(venue_id):
    new_venue=venue.query.filter_by(venue_id=venue_id).first()

    new_venue.venue_name=request.form.get('venue')
    new_venue.venue_place=request.form.get('place')
    new_venue.venue_location=request.form.get('location')
    new_venue.venue_capacity=request.form.get('capacity')


    from application.database import db
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/delete/venue/<int:venue_id>", methods=["GET"])
def delete_venue(venue_id):
    venue_details=venue.query.get(venue_id)
    show_venue_details=show_venue.query.filter_by(venue_id=venue_id).all()
    show_details=[show.query.filter_by(show_id=i.show_id).first() for i in show_venue_details]
    booking_details=sum((bookings.query.filter_by(show_id=i.show_id).all() for i in show_details), [])

    show_venue_available_tickets=[int(k.available_tickets) for k in show_venue_details]
    booking_details_booking_tickets=[int(j.booking_tickets) for j in booking_details]

    for i in show_venue_details:
        for j in booking_details_booking_tickets:
            i.available_tickets=i.available_tickets+j

    for k in show_venue_available_tickets:
        venue_details.venue_capacity=venue_details.venue_capacity+k
    
    from application.database import db

    db.session.delete(venue_details)
    if show_venue_details!=None:
        [db.session.delete(i) for i in show_venue_details]
    if show_details!=None:
        [db.session.delete(i) for i in show_details]
    if booking_details!=None:
        [db.session.delete(i) for i in booking_details]
        
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route("/create/show/<int:venue_id>", methods=["POST"])
def create_show(venue_id):

    venue_details=venue.query.filter_by(venue_id=venue_id).first()
    show_venue_details=show_venue.query.filter_by(venue_id=venue_id).first()
    
    show_name=request.form.get('show_name')
    show_timing=request.form.get('show_timing')
    show_tags=request.form.get('show_tags')
    show_ticketprice=request.form.get('show_price')
    show_available_tickets=request.form.get('available_tickets')

    venue_details.venue_capacity=venue_details.venue_capacity-int(show_available_tickets)

    if show_venue_details!=None:
        all_show_details=show.query.filter_by(show_id=show_venue_details.show_id).all()
        taken_timings=[i.show_timing for i in all_show_details]
        if show_timing in taken_timings:
            flash("Show timing already taken! Please select another time slot.", category='error')
            return redirect(url_for("admin_dashboard"))
        else:
            from application.database import db
            new_show=show(show_name=show_name, show_timing=show_timing, show_tags=show_tags, show_ticketprice=show_ticketprice)

            db.session.add(new_show)
            db.session.flush()
            db.session.refresh(new_show)

            new_show_venue=show_venue(show_id=new_show.show_id, venue_id=venue_id, available_tickets=show_available_tickets)
            db.session.add(new_show_venue)
            db.session.commit()
            return redirect(url_for("admin_dashboard"))
    else:
            from application.database import db
            new_show=show(show_name=show_name, show_timing=show_timing, show_tags=show_tags, show_ticketprice=show_ticketprice)

            db.session.add(new_show)
            db.session.flush()
            db.session.refresh(new_show)

            new_show_venue=show_venue(show_id=new_show.show_id, venue_id=venue_id, available_tickets=show_available_tickets)
            db.session.add(new_show_venue)
            db.session.commit()
            return redirect(url_for("admin_dashboard"))
    

@app.route("/edit/show/<int:show_id>", methods=["POST"])
def edit_show(show_id):
    new_show=show.query.filter_by(show_id=show_id).first()
    new_show_venue=show_venue.query.filter_by(show_id=show_id).first()
    venue_details=venue.query.filter_by(venue_id=new_show_venue.venue_id).first()

    venue_details.venue_capacity=venue_details.venue_capacity+int(new_show_venue.available_tickets)

    new_show.show_name=request.form.get('show_name')
    new_show.show_timing=request.form.get('show_timing')
    new_show.show_rating=request.form.get('show_rating')
    new_show.show_tags=request.form.get('show_tags')
    new_show.show_ticketprice=request.form.get('show_price')
    new_show_venue.available_tickets=request.form.get('available_tickets')

    venue_details.venue_capacity=venue_details.venue_capacity-int(new_show_venue.available_tickets)

    from application.database import db
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route("/delete/show/<int:show_id>", methods=["GET"])
def delete_show(show_id):

    show_details=show.query.filter_by(show_id=show_id).first()
    show_venue_details=show_venue.query.filter_by(show_id=show_id).first()
    booking_details=bookings.query.filter_by(show_id=show_venue_details.show_id).all()
    venue_details=venue.query.filter_by(venue_id=show_venue_details.venue_id).first()
    
    for i in booking_details:
        show_venue_details.available_tickets=show_venue_details.available_tickets+int(i.booking_tickets)
    venue_details.venue_capacity=venue_details.venue_capacity+int(show_venue_details.available_tickets)

    from application.database import db
    db.session.delete(show_details)
    if show_venue_details!=None:
        db.session.delete(show_venue_details)
    if booking_details!=None:
        [db.session.delete(i) for i in booking_details]
    db.session.commit()

    return redirect(url_for("admin_dashboard"))

@app.route("/create/booking/<int:show_id>", methods=["POST"])
def show_booking(show_id):
    show_venue_details=show_venue.query.filter_by(show_id=show_id).first()
    booking_tickets=request.form.get('booking_tickets')
    show_details=show.query.filter_by(show_id=show_id).first()

    show_venue_details.available_tickets=show_venue_details.available_tickets-int(booking_tickets)
    from application.database import db

    new_booking=bookings(booking_tickets=booking_tickets, user_id=current_user.id, show_id=show_details.show_id)
    db.session.add(new_booking)
    db.session.commit()
    return redirect(url_for("user_bookings"))

@app.route("/edit/booking/<int:booking_id>", methods=["POST"])
def edit_booking(booking_id):
    booking_details=bookings.query.filter_by(booking_id=booking_id).first()
    show_details=show.query.filter_by(show_id=booking_details.show_id).first()
    show_venue_details=show_venue.query.filter_by(show_id=show_details.show_id).first()

    show_venue_details.available_tickets=show_venue_details.available_tickets+booking_details.booking_tickets

    booking_details.booking_tickets=request.form.get('booking_tickets')

    show_venue_details.available_tickets=show_venue_details.available_tickets-int(booking_details.booking_tickets)

    from application.database import db
    db.session.commit()

    return redirect(url_for('user_bookings'))

@app.route("/delete/booking/<int:booking_id>", methods=["GET"])
#@login_required
def delete_booking(booking_id):
    booking_details=bookings.query.filter_by(booking_id=booking_id).first()
    show_details=show.query.filter_by(show_id=booking_details.show_id).first()
    show_venue_details=show_venue.query.filter_by(show_id=show_details.show_id).first()

    show_venue_details.available_tickets=show_venue_details.available_tickets+int(booking_details.booking_tickets)

    from application.database import db
    db.session.delete(booking_details)
    db.session.commit()
    return redirect(url_for('user_bookings'))

@app.route("/create/rating/<int:booking_id>", methods=["POST"])
#@login_required
def show_rating(booking_id):
    booking_details=bookings.query.filter_by(booking_id=booking_id).first()
    user_rating=request.form.get('rating')
    booking_details.user_rating=user_rating

    show_details=show.query.filter_by(show_id=booking_details.show_id).first()
    if show_details.show_rating==None:
        show_details.show_rating=int(user_rating)
    else:
        booking_details=bookings.query.filter_by(show_id=booking_details.show_id).all()
        total_rating=0
        total_count=0
        for booking_detail in booking_details:
            if booking_detail.user_rating is not None:
                total_rating+=int(booking_detail.user_rating)
                total_count+=1
        avg_rating=total_rating/total_count

        show_details.show_rating=int(avg_rating)

    from application.database import db
    db.session.commit()

    return redirect(url_for('user_bookings'))

