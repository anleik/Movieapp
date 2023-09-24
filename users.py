from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash



def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            return True
        else:
            return False

def user_id(username):
    check_username_sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(check_username_sql, {"username":username})
    user = result.fetchone()
    return user[0]

def logout():
    del session["user_id"]

def register(username, password):
    check_username_sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(check_username_sql, {"username":username})
    existing_user = result.fetchone()

    if existing_user:
        return False

    hash_value = generate_password_hash(password)
    
    sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, 'f')")
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()
    return login(username, password)


