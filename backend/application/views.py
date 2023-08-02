from flask import request
from .models import *
from flask import current_app as app
from passlib.hash import pbkdf2_sha256 as passhash
import jwt, secrets,datetime
# from application.cache import cache
# import matplotlib
# import matplotlib.pyplot as plt

# matplotlib.use("Agg")

@app.route("/api/register", methods=['POST'])
def userRegister():
    data=request.get_json()
    username=data.get("username")
    email=data.get("email")
    password=data.get("password")

    new_user=User(email=email,username=username,password=passhash.hash(password))
    db.session.add(new_user)
    db.session.commit()

    token = Token(user_id=new_user.id, token=secrets.token_urlsafe(32))
    db.session.add(token)
    db.session.commit()

    # cache.clear()
    token=token.token
    encoded = jwt.encode({"token": token}, app.secret_key)
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    return {"token": encoded, "expiry": expiry_time}

@app.route("/api/login",methods=["POST"])
def userLogin():
    data=request.get_json()
    (email,password) = (data.get("email"),data.get("password"))
    current_user=User.query.filter_by(email=email).first()
    if not current_user:
        return {"Error" : 404, "errorMessage": "User not found"}
    if not passhash.verify(password,current_user.password):
        return {"Error" : 401, "errorMessage": "Invalid Password"}
    
    token=Token.query.filter_by(user_id=current_user.id).first().token
    encoded_token = jwt.encode({"token": token}, app.secret_key)
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    return {"token": encoded_token, "expiry": expiry_time}

@app.route("/api/venues", methods=["GET","POST"])
def allVenues():
    if request.method=="GET":
        venues=Venues.query.all()
        return [venue.to_dict() for venue in venues]
    
    if request.method=="POST":
        data=request.get_json()
        venue_name=data.get("venue_name")
        venue_place=data.get("venue_place")
        venue_location=data.get("venue_location")
        venue_capacity=data.get("venue_capacity")

        new_venue=Venues(venue_name=venue_name, venue_place=venue_place, venue_location=venue_location, venue_capacity=venue_capacity)
        db.session.add(new_venue)
        db.session.commit()
        return "Venue Created!"

@app.route("/api/venue/<int:venue_id>",methods=["PUT","PATCH","DELETE"])
def theVenues(venue_id):
    if request.method=="DELETE":
        the_venue=Venues.query.filter_by(venue_id=venue_id).first()
        db.session.delete(the_venue)
        db.session.commit()
        return "FUCKING VENUE DELETED"

@app.route("/api/shows",methods=["GET","POST"])
def allShows():
    if request.method=="GET":
        shows=Shows.query.all()
        return [show.to_dict() for show in shows]
    
    if request.method=="POST":
        data=request.get_json()
        venue_id=data.get("venue_id")
        show_name=data.get("show_name")
        show_timing=data.get("show_timing")
        show_tags=data.get("show_tags")
        show_ticketprice=data.get("show_ticketprice")
        available_tickets=data.get("available_tickets")

        new_show=Shows(show_name=show_name, show_timing=show_timing, show_tags=show_tags, show_rating="NA", show_ticketprice=show_ticketprice)

        db.session.add(new_show)
        db.session.flush()
        db.session.refresh(new_show)

        new_show_venue=ShowVenue(show_id=new_show.show_id, venue_id=venue_id, available_tickets=available_tickets)
        db.session.add(new_show_venue)
        db.session.commit()
        return "Success MF"

@app.route("/api/show/<int:show_id>",methods=["PUT","PATCH","DELETE"])
def theShows(show_id):
    if request.method=="DELETE":
        
        the_show=Shows.query.filter_by(show_id=show_id).first()
        db.session.delete(the_show)
        db.session.commit()
        return "FUCKING DELETED"

@app.route("/api/bookings/<int:show_id>", methods=["POST","PUT","DELETE"])
def booking(show_id):
    if request.method=="POST":
        data=request.get_json()
        booking_tickets=data.get("tickets")

        # new_booking=Bookings(booking_tickets=booking_tickets, user_id=current_user.id, show_id=show_id)
        return 'data'
    

# @app.route('/user_dashboard/search', methods=["GET"])
# def search():
#     venues=Venues.query.all()
#     shows=show.query.all()
#     show_venues=show_venue.query.all()

#     search_by_category=['Show','Venue','Location','Timing', 'Genre','Rating' ]

#     search_value=request.args.get('search_value')
#     search_query=request.args.get('search_query')
#     query="%"+search_query+"%"
    
#     available_locations=[ html.escape(i[0],quote=True) for i in db.session.query(venue.venue_location.distinct()).all()]
#     available_genres=[ html.escape(i[0],quote=True) for i in db.session.query(show.show_tags.distinct()).all()]
#     available_timings=[ html.escape(i[0],quote=True) for i in db.session.query(show.show_timing.distinct()).all()]
#     available_shows=[ html.escape(i[0],quote=True) for i in db.session.query(show.show_name.distinct()).all()]
#     available_venues=[ html.escape(i[0],quote=True) for i in db.session.query(venue.venue_name.distinct()).all()]

#     if search_value=="Show":
#         results=show.query.filter(show.show_name.like(query)).all()
#     elif search_value=="Venue":
#         results=venue.query.filter(venue.venue_name.like(query)).all()
#     elif search_value=="Location":
#         results=venue.query.filter(venue.venue_location.like(query)).all()
#     elif search_value=="Timing":
#         results=show.query.filter(show.show_timing.like(query)).all()
#     elif search_value=="Genre":
#         results=show.query.filter(show.show_tags.like(query)).all()
#     elif search_value=="Rating":
#         results=show.query.filter(show.show_rating.like(query)).all()
    
#     return render_template('search.html', venues=venues, shows=shows, show_venues=show_venues,search_by_category=search_by_category,search_value=search_value,search_query=search_query,available_locations=available_locations,available_genres=available_genres,available_timings=available_timings,available_shows=available_shows,available_venues=available_venues,results=results)


# @app.route("/admin_summary", methods=["GET", "POST"])
# def admin_summary():
#     show_venues=show_venue.query.all()
#     x=[]
#     y=[]
#     for i in show_venues:
#         show_details=show.query.filter_by(show_id=i.show_id).first()
#         x.append(show_details.show_name)
#         y.append(i.available_tickets)


#     plt.bar(x,y, width=0.5)
#     plt.xlabel('Show Name')
#     plt.ylabel('Available Tickets')
    
#     plt.savefig(f"./static/{current_user.id}_show_venue.png")
#     plt.clf()

#     venues=venue.query.all()
#     x=[]
#     y=[]
#     for i in venues:
#         venue_details=venue.query.filter_by(venue_id=i.venue_id).first()
#         x.append(venue_details.venue_name)
#         y.append(i.venue_capacity)

#     print(x,y)
#     plt.bar(x,y, width=0.5)
#     plt.xlabel('Venue Name')
#     plt.ylabel('Venue Capacity')
    
#     plt.savefig(f"./static/{current_user.id}_venue.png")
#     plt.clf()

#     return render_template("admin_summary.html")

# @app.route("/create/venue", methods=["POST"])
# def create_venue():
#     venue_name=request.form.get('venue')
#     venue_place=request.form.get('place')
#     venue_location=request.form.get('location')
#     venue_capacity=request.form.get('capacity')

#     from application.database import db
#     new_venue=venue(venue_name=venue_name, venue_place=venue_place, venue_location=venue_location, venue_capacity=venue_capacity)

#     db.session.add(new_venue)
#     db.session.commit()

#     return "Success",200

# @app.route("/edit/venue/<int:venue_id>", methods=["POST"])
# def edit_venue(venue_id):
#     new_venue=venue.query.filter_by(venue_id=venue_id).first()

#     new_venue.venue_name=request.form.get('venue')
#     new_venue.venue_place=request.form.get('place')
#     new_venue.venue_location=request.form.get('location')
#     new_venue.venue_capacity=request.form.get('capacity')


#     from application.database import db
#     db.session.commit()
#     return redirect(url_for("admin_dashboard"))

# @app.route("/delete/venue/<int:venue_id>", methods=["GET"])
# def delete_venue(venue_id):
#     venue_details=venue.query.get(venue_id)
#     show_venue_details=show_venue.query.filter_by(venue_id=venue_id).all()
#     show_details=[show.query.filter_by(show_id=i.show_id).first() for i in show_venue_details]
#     booking_details=sum((bookings.query.filter_by(show_id=i.show_id).all() for i in show_details), [])

#     show_venue_available_tickets=[int(k.available_tickets) for k in show_venue_details]
#     booking_details_booking_tickets=[int(j.booking_tickets) for j in booking_details]

#     for i in show_venue_details:
#         for j in booking_details_booking_tickets:
#             i.available_tickets=i.available_tickets+j

#     for k in show_venue_available_tickets:
#         venue_details.venue_capacity=venue_details.venue_capacity+k
    
#     from application.database import db

#     db.session.delete(venue_details)
#     if show_venue_details!=None:
#         [db.session.delete(i) for i in show_venue_details]
#     if show_details!=None:
#         [db.session.delete(i) for i in show_details]
#     if booking_details!=None:
#         [db.session.delete(i) for i in booking_details]
        
#     db.session.commit()
#     return redirect(url_for('admin_dashboard'))

# @app.route("/create/show/<int:venue_id>", methods=["POST"])
# def create_show(venue_id):

#     venue_details=venue.query.filter_by(venue_id=venue_id).first()
#     show_venue_details=show_venue.query.filter_by(venue_id=venue_id).first()
    
#     show_name=request.form.get('show_name')
#     show_timing=request.form.get('show_timing')
#     show_tags=request.form.get('show_tags')
#     show_ticketprice=request.form.get('show_price')
#     show_available_tickets=request.form.get('available_tickets')

#     venue_details.venue_capacity=venue_details.venue_capacity-int(show_available_tickets)

#     if show_venue_details!=None:
#         all_show_details=show.query.filter_by(show_id=show_venue_details.show_id).all()
#         taken_timings=[i.show_timing for i in all_show_details]
#         if show_timing in taken_timings:
#             flash("Show timing already taken! Please select another time slot.", category='error')
#             return redirect(url_for("admin_dashboard"))
#         else:
#             from application.database import db
#             new_show=show(show_name=show_name, show_timing=show_timing, show_tags=show_tags, show_ticketprice=show_ticketprice)

#             db.session.add(new_show)
#             db.session.flush()
#             db.session.refresh(new_show)

#             new_show_venue=show_venue(show_id=new_show.show_id, venue_id=venue_id, available_tickets=show_available_tickets)
#             db.session.add(new_show_venue)
#             db.session.commit()
#             return redirect(url_for("admin_dashboard"))
#     else:
#             from application.database import db
#             new_show=show(show_name=show_name, show_timing=show_timing, show_tags=show_tags, show_ticketprice=show_ticketprice)

#             db.session.add(new_show)
#             db.session.flush()
#             db.session.refresh(new_show)

#             new_show_venue=show_venue(show_id=new_show.show_id, venue_id=venue_id, available_tickets=show_available_tickets)
#             db.session.add(new_show_venue)
#             db.session.commit()
#             return redirect(url_for("admin_dashboard"))
    

# @app.route("/edit/show/<int:show_id>", methods=["POST"])
# def edit_show(show_id):
#     new_show=show.query.filter_by(show_id=show_id).first()
#     new_show_venue=show_venue.query.filter_by(show_id=show_id).first()
#     venue_details=venue.query.filter_by(venue_id=new_show_venue.venue_id).first()

#     venue_details.venue_capacity=venue_details.venue_capacity+int(new_show_venue.available_tickets)

#     new_show.show_name=request.form.get('show_name')
#     new_show.show_timing=request.form.get('show_timing')
#     new_show.show_rating=request.form.get('show_rating')
#     new_show.show_tags=request.form.get('show_tags')
#     new_show.show_ticketprice=request.form.get('show_price')
#     new_show_venue.available_tickets=request.form.get('available_tickets')

#     venue_details.venue_capacity=venue_details.venue_capacity-int(new_show_venue.available_tickets)

#     from application.database import db
#     db.session.commit()
#     return redirect(url_for('admin_dashboard'))

# @app.route("/delete/show/<int:show_id>", methods=["GET"])
# def delete_show(show_id):

#     show_details=show.query.filter_by(show_id=show_id).first()
#     show_venue_details=show_venue.query.filter_by(show_id=show_id).first()
#     booking_details=bookings.query.filter_by(show_id=show_venue_details.show_id).all()
#     venue_details=venue.query.filter_by(venue_id=show_venue_details.venue_id).first()
    
#     for i in booking_details:
#         show_venue_details.available_tickets=show_venue_details.available_tickets+int(i.booking_tickets)
#     venue_details.venue_capacity=venue_details.venue_capacity+int(show_venue_details.available_tickets)

#     from application.database import db
#     db.session.delete(show_details)
#     if show_venue_details!=None:
#         db.session.delete(show_venue_details)
#     if booking_details!=None:
#         [db.session.delete(i) for i in booking_details]
#     db.session.commit()

#     return redirect(url_for("admin_dashboard"))

# @app.route("/create/booking/<int:show_id>", methods=["POST"])
# def show_booking(show_id):
#     show_venue_details=show_venue.query.filter_by(show_id=show_id).first()
#     booking_tickets=request.form.get('booking_tickets')
#     show_details=show.query.filter_by(show_id=show_id).first()

#     show_venue_details.available_tickets=show_venue_details.available_tickets-int(booking_tickets)
#     from application.database import db

#     new_booking=bookings(booking_tickets=booking_tickets, user_id=current_user.id, show_id=show_details.show_id)
#     db.session.add(new_booking)
#     db.session.commit()
#     return redirect(url_for("user_bookings"))

# @app.route("/edit/booking/<int:booking_id>", methods=["POST"])
# def edit_booking(booking_id):
#     booking_details=bookings.query.filter_by(booking_id=booking_id).first()
#     show_details=show.query.filter_by(show_id=booking_details.show_id).first()
#     show_venue_details=show_venue.query.filter_by(show_id=show_details.show_id).first()

#     show_venue_details.available_tickets=show_venue_details.available_tickets+booking_details.booking_tickets

#     booking_details.booking_tickets=request.form.get('booking_tickets')

#     show_venue_details.available_tickets=show_venue_details.available_tickets-int(booking_details.booking_tickets)

#     from application.database import db
#     db.session.commit()

#     return redirect(url_for('user_bookings'))

# @app.route("/delete/booking/<int:booking_id>", methods=["GET"])
# #@login_required
# def delete_booking(booking_id):
#     booking_details=bookings.query.filter_by(booking_id=booking_id).first()
#     show_details=show.query.filter_by(show_id=booking_details.show_id).first()
#     show_venue_details=show_venue.query.filter_by(show_id=show_details.show_id).first()

#     show_venue_details.available_tickets=show_venue_details.available_tickets+int(booking_details.booking_tickets)

#     from application.database import db
#     db.session.delete(booking_details)
#     db.session.commit()
#     return redirect(url_for('user_bookings'))

# @app.route("/create/rating/<int:booking_id>", methods=["POST"])
# #@login_required
# def show_rating(booking_id):
#     booking_details=bookings.query.filter_by(booking_id=booking_id).first()
#     user_rating=request.form.get('rating')
#     booking_details.user_rating=user_rating

#     show_details=show.query.filter_by(show_id=booking_details.show_id).first()
#     if show_details.show_rating==None:
#         show_details.show_rating=int(user_rating)
#     else:
#         booking_details=bookings.query.filter_by(show_id=booking_details.show_id).all()
#         total_rating=0
#         total_count=0
#         for booking_detail in booking_details:
#             if booking_detail.user_rating is not None:
#                 total_rating+=int(booking_detail.user_rating)
#                 total_count+=1
#         avg_rating=total_rating/total_count

#         show_details.show_rating=int(avg_rating)

#     from application.database import db
#     db.session.commit()

#     return redirect(url_for('user_bookings'))

