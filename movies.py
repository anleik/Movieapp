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

def movie_name(title):
    sql = text("SELECT * FROM movies WHERE name = :title")
    result = db.session.execute(sql, {'title': title})
    movie = result.fetchone()
    return movie

def movie_genres(movie_id):
    sql = text("""
        SELECT g.name 
        FROM genres g 
        JOIN movie_genres mg 
        ON g.id = mg.genre_id 
        WHERE movie_id = :id
        """)
    result = db.session.execute(sql, {'id':movie_id})
    movie_genres = [row[0] for row in result]
    return movie_genres

def avg_score(movie_id):
    sql = text("SELECT AVG(score) FROM reviews WHERE movie_id = :movie_id")
    result = db.session.execute(sql, {'movie_id':movie_id})
    return result.scalar()
