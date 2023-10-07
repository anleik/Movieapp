from db import db
from flask import session
from sqlalchemy.sql import text



def add_movie(name, year):
    sql = text("INSERT INTO movies (name, year) VALUES (:name, :year)")
    db.session.execute(sql, {"name":name, "year":year})
    db.session.commit()
    return True

def add_genre(name):
    sql = text("INSERT INTO genres (name) VALUES (:name)")
    db.session.execute(sql, {"name":name})
    db.session.commit()
    return True

def link_genre(movie, genre):
    sql = text("INSERT INTO movie_genres (movie_id, genre_id) VALUES (:movie, :genre)")
    db.session.execute(sql, {"movie":movie, "genre":genre})
    db.session.commit()
    return True

def get_movies():
    sql = text("SELECT * FROM movies")
    result = db.session.execute(sql)
    return result.fetchall()

def get_genres():
    sql = text("SELECT * FROM genres")
    result = db.session.execute(sql)
    return result.fetchall()
