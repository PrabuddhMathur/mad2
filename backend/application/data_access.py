from application.models import *
from application.cache import cache

@cache.memoize()
def get_all_venues():
    all_venues=Venues.query.all()
    return [venue.to_dict() for venue in all_venues]

@cache.memoize()
def get_all_shows():
    all_shows=Shows.query.all()
    return all_shows

@cache.memoize()
def get_all_users():
    users=User.query.all()
    return users

@cache.memoize()
def get_user_by_id(user_id):
    user=User.query.filter_by(id=user_id).first()
    return user

@cache.memoize()
def get_status(user_id):
    visited=Visited.query.filter_by(user_id=user_id).first()
    return visited

@cache.memoize()
def get_user_bookings(user_id):
    bookings=Bookings.query.filter_by(user_id=user_id).all()
    return bookings

@cache.memoize()
def get_showvenue_by_show_id(show_id):
    showvenue=ShowVenue.query.filter_by(show_id=show_id).first()
    return showvenue

@cache.memoize()
def get_showvenue_by_venue_id(venue_id):
    showvenue=ShowVenue.query.filter_by(venue_id=venue_id).first()
    return showvenue

@cache.memoize()
def get_bookings_by_id(booking_id):
    booking=Bookings.query.filter_by(booking_id=booking_id).first()
    return booking

@cache.memoize()
def get_bookings_by_show_id(show_id):
    bookings=Bookings.query.filter_by(show_id=show_id).all()
    return bookings

@cache.memoize()
def get_venue_by_id(venue_id):
    venue=Venues.query.filter_by(venue_id=venue_id).first()
    return venue

@cache.memoize()
def get_venue_by_show_id(show_id):
    venue_id=ShowVenue.query.filter_by(show_id=show_id).first().venue_id
    venue=Venues.query.filter_by(venue_id=venue_id).first()
    return venue

@cache.memoize()
def get_show_by_id(show_id):
    show=Shows.query.filter_by(show_id=show_id).first()
    return show

@cache.memoize()
def get_shows_by_venue_id(venue_id):
    shows=ShowVenue.query.filter_by(venue_id=venue_id).all()
    show_id=[i.show_id for i in shows]
    shows=[Shows.query.filter_by(show_id=i).first() for i in show_id]
    return [shows,show_id]

@cache.memoize()
def get_user_by_email(email):
    user=User.query.filter_by(email=email).first()
    return user

@cache.memoize()
def get_token_by_user_id(user_id):
    token=Token.query.filter_by(user_id=user_id).first().token
    return token

@cache.memoize()
def get_user_id_by_token(token):
    user_id=Token.query.filter_by(token=token).first().user_id
    return user_id




