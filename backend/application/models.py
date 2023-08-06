from .database import *

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    email=db.Column(db.String, unique=True)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.String(255))
    isadmin=db.Column(db.Boolean,nullable=False,default=False)

class Shows(db.Model):
    __tablename__='shows'
    show_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_name=db.Column(db.String)
    show_timing=db.Column(db.String)
    show_rating=db.Column(db.Integer)
    show_tags=db.Column(db.String)
    show_ticketprice=db.Column(db.Integer)

    def to_dict(self):
        this_venue=ShowVenue.query.filter_by(show_id=self.show_id).first()
        venue_details=Venues.query.filter_by(venue_id=this_venue.venue_id).first()
        available_tickets=ShowVenue.query.filter_by(show_id=self.show_id).first().available_tickets
        
        return {
            "show_id":self.show_id,
            "show_name":self.show_name,
            "show_timing":self.show_timing,
            "show_rating":self.show_rating,
            "show_tags":self.show_tags,
            "show_ticketprice":self.show_ticketprice,
            "available_tickets":available_tickets,
            "venue":[venue_details.to_show_dict()]
        }
    
class Venues(db.Model):
    __tablename__='venues'
    venue_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_name=db.Column(db.String, unique=True)
    venue_place=db.Column(db.String)
    venue_location=db.Column(db.String)
    venue_capacity=db.Column(db.Integer)
    venue_show=db.relationship(Shows, secondary="show_venue", backref="show_venue")
    
    def to_show_dict(self):
        return {
            "venue_id":self.venue_id,
            "venue_name":self.venue_name,
            "venue_place":self.venue_place,
            "venue_location":self.venue_location,
            "venue_capacity":self.venue_capacity
        }

    def to_dict(self):
        venue_show=[i.to_dict() for i in self.venue_show]
        tickets = [i.to_dict()["available_tickets"] for j in [k.to_dict() for k in self.venue_show] for i in ShowVenue.query.filter_by(venue_id=self.venue_id, show_id=j["show_id"]).all()]
        v = []
        for i, show in enumerate(venue_show):
            show["available_tickets"] = tickets[i]
            v.append(show)
        return {
            "venue_id":self.venue_id,
            "venue_name":self.venue_name,
            "venue_place":self.venue_place,
            "venue_location":self.venue_location,
            "venue_capacity":self.venue_capacity,
             "venue_show": v
        }
    
class Bookings(db.Model):
    __tablename__="bookings"
    booking_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    booking_tickets=db.Column(db.Integer, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    show_id=db.Column(db.Integer, db.ForeignKey("shows.show_id"), nullable=False)
    user_rating=db.Column(db.Integer)

    
    def to_dict(self):
        venue_id=ShowVenue.query.filter_by(show_id=self.show_id).first().venue_id
        venue_details=Venues.query.filter_by(venue_id=venue_id).first().to_dict()

        show_details=Shows.query.filter_by(show_id=self.show_id).first().to_dict()
        return {
            "booking_id":self.booking_id,
            "booking_tickets":self.booking_tickets,
            "user_id":self.user_id,
            "show_id":self.show_id,
            "user_rating":self.user_rating,
            "venue_details":venue_details,
            "show_details":show_details
        }

class ShowVenue(db.Model):
    __tablename__='show_venue'
    show_venue_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_id=db.Column(db.Integer, db.ForeignKey("shows.show_id"), nullable=False)
    venue_id=db.Column(db.Integer, db.ForeignKey("venues.venue_id"), nullable=False)
    available_tickets=db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "show_venue_id":self.show_venue_id,
            "show_id":self.show_id,
            "venue_id":self.venue_id,
            "available_tickets":self.available_tickets
        }
    
class Token(db.Model):
    __tablename__ = "token"
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)