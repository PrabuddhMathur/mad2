from flask import request, send_file
from .models import *
from flask import current_app as app
from passlib.hash import pbkdf2_sha256 as passhash
import jwt, secrets,datetime
from application.cache import cache
from application.data_access import *
import matplotlib
import matplotlib.pyplot as plt
from application import tasks

matplotlib.use("Agg")

@app.route("/api/register", methods=['POST'])
def userRegister():
    data=request.get_json()
    username=data.get("username")
    email=data.get("email")
    password=data.get("password")

    if get_user_by_email(email):
        return {"Error" : 401, "errorMessage": "Email already exists."}
    new_user=User(email=email,username=username,password=passhash.hash(password))
    db.session.add(new_user)
    db.session.commit()

    token = Token(user_id=new_user.id, token=secrets.token_urlsafe(32))
    db.session.add(token)
    db.session.commit()

    visit=Visited(user_id=new_user.id, status=True)
    db.session.add(visit)
    db.session.commit()

    cache.clear()
    token=token.token
    encoded = jwt.encode({"token": token}, app.secret_key)
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    return {"token": encoded, "expiry": expiry_time}

@app.route("/api/login",methods=["POST"])
def userLogin():
    data=request.get_json()
    (email,password) = (data.get("email"),data.get("password"))
    current_user=get_user_by_email(email)
    
    if not current_user:
        return {"Error" : 404, "errorMessage": "User not found"}
    if not passhash.verify(password,current_user.password):
        return {"Error" : 401, "errorMessage": "Invalid Password"}
    
    token=get_token_by_user_id(current_user.id)
    encoded_token = jwt.encode({"token": token}, app.secret_key)
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)

    get_status(current_user.id).status=True
    
    db.session.commit()


    return {"token": encoded_token, "expiry": expiry_time}

@app.route("/api/isadmin")
def isAdmin():
    token=request.headers.get("Authorization", "").split(" ")[-1]
    if not token:
        return [False]

    decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])

    user_id=get_user_id_by_token(decodedToken['token'])
    
    isAdmin=User.query.filter_by(id=user_id).first().isadmin
    return [isAdmin]

@app.route("/api/username")
def username():
    token=request.headers.get("Authorization", "").split(" ")[-1]
    if not token:
        return [False]
    decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
    user_id=get_user_id_by_token(decodedToken['token'])
    user_name=get_user_by_id(user_id).username
    return user_name

@app.route("/api/venues", methods=["GET","POST"])
def allVenues():
    if request.method=="GET":
        # tasks.helloWorld.delay()
        venues=get_all_venues()
        return venues

    if request.method=="POST":
        data=request.get_json()
        venue_name=data.get("venue_name")
        venue_place=data.get("venue_place")
        venue_location=data.get("venue_location")
        venue_capacity=data.get("venue_capacity")

        new_venue=Venues(venue_name=venue_name, venue_place=venue_place, venue_location=venue_location, venue_capacity=venue_capacity)
        db.session.add(new_venue)
        db.session.commit()
        cache.clear()
        return "Venue Created!"

@app.route("/api/venue/<int:venue_id>",methods=["PUT","DELETE"])
def theVenues(venue_id):
    if request.method=="PUT":
        data=request.get_json()

        updated_venue=get_venue_by_id(venue_id)
        updated_venue.venue_name=data.get('updated_venue_name')
        updated_venue.venue_capacity=data.get('updated_venue_capacity')
        updated_venue.venue_place=data.get('updated_venue_place')
        updated_venue.venue_location=data.get('updated_venue_location')

        db.session.commit()
        cache.clear()

        return "UPDATED!"
    if request.method=="DELETE":
        cache.clear()
        the_venue=get_venue_by_id(venue_id)
        the_shows=get_shows_by_venue_id(venue_id)[0]
        the_show_ids=get_shows_by_venue_id(the_venue.venue_id)[1]
        all_bookings=[get_bookings_by_show_id(i) for i in the_show_ids]
        the_bookings=[booking for bookings in all_bookings for booking in bookings]

        db.session.delete(the_venue)
        if the_shows!=[]:
            [db.session.delete(i) for i in the_shows]
        if the_bookings!=[]:
            [db.session.delete(i) for i in the_bookings]
        db.session.commit()
        
        return "FUCKING VENUE DELETED"

@app.route("/api/shows",methods=["GET","POST"])
def allShows():
    if request.method=="GET":
        shows=get_all_shows()
        return [show.to_dict() for show in shows]
    
    if request.method=="POST":
        data=request.get_json()
        venue_id=data.get("venue_id")
        show_name=data.get("show_name")
        show_timing=data.get("show_timing")
        show_tags=data.get("show_tags")
        show_ticketprice=data.get("show_ticketprice")
        available_tickets=data.get("available_tickets")

        venue_details=get_venue_by_id(venue_id)
        venue_details.venue_capacity=venue_details.venue_capacity-available_tickets
        new_show=Shows(show_name=show_name, show_timing=show_timing, show_tags=show_tags, show_rating="NA", show_ticketprice=show_ticketprice)

        db.session.add(new_show)
        db.session.flush()
        db.session.refresh(new_show)

        new_show_venue=ShowVenue(show_id=new_show.show_id, venue_id=venue_id, available_tickets=available_tickets)
        db.session.add(new_show_venue)
        db.session.commit()
        cache.clear()
        return "Success MF"

@app.route("/api/show/<int:show_id>",methods=["GET","PUT","DELETE"])
def theShows(show_id):
    if request.method=="GET":
        show=get_show_by_id(show_id)
        return show.to_dict()
        
    if request.method=="DELETE":
        cache.clear()
        the_show=get_show_by_id(show_id)
        all_bookings=get_bookings_by_show_id(show_id)

        bookings=[i.booking_tickets for i in all_bookings]
        the_venue=get_venue_by_show_id(show_id)
        show_venue_details=get_showvenue_by_show_id(show_id)
        the_venue.venue_capacity=the_venue.venue_capacity+sum(bookings)+show_venue_details.available_tickets

        db.session.delete(the_show)
        db.session.delete(show_venue_details)

        if all_bookings!=None:
            [db.session.delete(i) for i in all_bookings]
        db.session.commit()
        
        return "Show Deleted Successfully"
    
    if request.method=="PUT":
        data=request.get_json()

        show_details=get_show_by_id(show_id)
        venue_details=get_venue_by_show_id(show_id)
        show_venue_details=get_showvenue_by_show_id(show_id)

        venue_details.venue_capacity+=show_venue_details.available_tickets

        show_details.show_name=data.get('updated_name')
        show_details.show_timing=data.get('updated_timing')
        show_details.show_tags=data.get('updated_genre')
        show_details.show_ticketprice=data.get('updated_show_price')
        show_venue_details.available_tickets=data.get('updated_tickets')

        venue_details.venue_capacity-=show_venue_details.available_tickets

        db.session.commit()
        cache.clear()

        return "UPDATED!"

@app.route("/api/bookings", methods=["GET","POST","PUT"])
def bookings():
    if request.method=="GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
        user_id=get_user_id_by_token(decodedToken['token'])
        
        bookings=get_user_bookings(user_id)

        return [booking.to_dict() for booking in bookings]

    if request.method=="POST":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
        user_id=get_user_id_by_token(decodedToken['token'])

        data=request.get_json()
        booking_tickets=data.get("tickets")
        show_id=data.get("show_id")

        show_venue_details=get_showvenue_by_show_id(show_id)
        show_venue_details.available_tickets-=booking_tickets

        showname=get_show_by_id(show_id).show_name
        username=get_user_by_id(user_id).username
        email=get_user_by_id(user_id).email

        new_booking=Bookings(booking_tickets=booking_tickets, user_id=user_id, show_id=show_id)
        db.session.add(new_booking)
        db.session.commit()
        tasks.send_booking_mail.delay(showname,username,booking_tickets,email)
        cache.clear()

        return 'data'
    
    if request.method=="PUT":
        cache.clear()

        data=request.get_json()
        booking_tickets=data.get("tickets")
        booking_id=data.get("booking_id")

        the_booking=get_bookings_by_id(booking_id)
        show_booking_details=get_showvenue_by_show_id(the_booking.show_id)

        show_booking_details.available_tickets+=the_booking.booking_tickets
        
        the_booking.booking_tickets=booking_tickets

        show_booking_details.available_tickets-=the_booking.booking_tickets

        db.session.commit()
        return 'Booking Updated!'

@app.route("/api/bookings/<int:booking_id>",methods=["DELETE"])
def delBookings(booking_id):
    booking_details=get_bookings_by_id(booking_id)
    show_venue_details=get_showvenue_by_show_id(booking_details.show_id)
    show_venue_details.available_tickets+=booking_details.booking_tickets

    db.session.delete(booking_details)
    db.session.commit()
    cache.clear()
    return "BOOKING DELETED"

@app.route("/api/search",methods=["POST"])
def search():
    data=request.get_json()
    search_category=data.get("category")
    search_query=data.get("query")
    query="%"+search_query+"%"

    if search_category=="Show":
        results=Shows.query.filter(Shows.show_name.like(query)).all()
    elif search_category=="Venue":
        results=Venues.query.filter(Venues.venue_name.like(query)).all()
    elif search_category=="Location":
        results=Venues.query.filter(Venues.venue_location.like(query)).all()
    elif search_category=="Timing":
        results=Shows.query.filter(Shows.show_timing.like(query)).all()
    elif search_category=="Genre":
        results=Shows.query.filter(Shows.show_tags.like(query)).all()
    elif search_category=="Rating":
        results=Shows.query.filter(Shows.show_rating.like(query)).all()
    
    return [i.to_dict() for i in results]

@app.route("/api/rating", methods=["GET", "POST"])
def rating():
    if request.method=="POST":
        cache.clear()
        data=request.get_json()

        updated_rating=data.get('rating')
        booking_id=data.get('booking_id')

        the_booking=get_bookings_by_id(booking_id)

        the_booking.user_rating=updated_rating
        all_bookings=get_bookings_by_show_id(the_booking.show_id)
        total_rating=0
        total_count=0
        for booking_detail in all_bookings:
            if booking_detail.user_rating is not None:
                total_rating+=int(booking_detail.user_rating)
                total_count+=1
        avg_rating=total_rating/total_count
        
        show_details=get_show_by_id(the_booking.show_id)
        show_details.show_rating=int(avg_rating)

        db.session.commit()
        cache.clear()
    return "Rating Created"

@app.route("/static/<filename>")
def serve_static(filename):
    file="./static/" + filename
    return send_file(file,mimetype='image/png')

@app.route("/api/admin_summary")
def summary():

    all_shows=get_all_shows()
    x=[i.show_name for i in all_shows]
    y=[i.to_dict()['available_tickets'] for i in all_shows]

    plt.bar(x,y,width=0.5)
    plt.xlabel('Show Name')
    plt.ylabel('Available Tickets')
    plt.savefig(f"./static/show_details.png")
    plt.clf()

    all_venues=get_all_venues()
    a=[i['venue_name'] for i in all_venues]
    b=[i['venue_capacity'] for i in all_venues]

    plt.bar(a,b,width=0.5)
    plt.xlabel('Venue Name')
    plt.ylabel('Venue Capacity')
    plt.savefig(f"./static/venue_details.png")
    plt.clf()

    return "Admin Summary Created"

@app.route("/api/export/<int:venue_id>")
def export(venue_id):
    token=request.headers.get("Authorization", "").split(" ")[-1]
    decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
    user_id=get_user_id_by_token(decodedToken['token'])

    tasks.export_venue_csv.delay(venue_id,user_id)
    return "Venue details successfully exported and sent via mail."
