from db import db
from flask import session
from sqlalchemy.sql import text



def add_movie(name, year):
    sql = text("INSERT INTO movies (name, year) VALUES (:name, :year)")
    db.session.execute(sql, {"name":name, "year":year})
    db.session.commit()
    return True
