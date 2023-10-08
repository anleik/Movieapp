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

def get_user_by_id(user_id):
    sql = text("SELECT * FROM users WHERE id = :id")
    result = db.session.execute(sql, {'id':user_id})
    user = result.fetchone()
    return user

def is_admin(username):
    check_admin_sql = text("SELECT admin FROM users WHERE username = :username")
    result = db.session.execute(check_admin_sql, {"username": username})
    admin = result.fetchone()
    return admin[0]

def logout():
    del session["user_id"]

def register(username, password, is_admin):
    check_username_sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(check_username_sql, {"username":username})
    existing_user = result.fetchone()

    if existing_user:
        return False

    hash_value = generate_password_hash(password)
    
    sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :is_admin)")
    db.session.execute(sql, {"username": username, "password": hash_value, "is_admin": is_admin})
    db.session.commit()
    return login(username, password)


