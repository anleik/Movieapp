from db import db
from flask import session
from sqlalchemy.sql import text




def review(score, content, username, movie):
    check_username_sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(check_username_sql, {"username":username})
    user = result.fetchone()

    if not user:
        return False
    
    check_user_review_sql = text("SELECT user_id, movie_id FROM reviews WHERE user_id = :user_id AND movie_id = :movie_id")
    result2 = db.session.execute(check_user_review_sql, {"user_id":user[0], "movie_id":movie.id})
    user_review = result2.fetchone()

    if user_review:
        return False

    sql = text("INSERT INTO reviews (content, score, user_id, movie_id) VALUES (:content, :score, :user, :movie)")
    db.session.execute(sql, {"content":content,"score":score,"user":user[0],"movie":movie.id})
    db.session.commit()
    return True

def delete_review(review_id):
    delete_likes_sql = text("DELETE FROM likes WHERE review_id = :review_id")
    db.session.execute(delete_likes_sql, {"review_id":review_id})
    db.session.commit()
    delete_review_sql = text("DELETE FROM reviews WHERE id = :review_id")
    db.session.execute(delete_review_sql, {"review_id":review_id})
    db.session.commit()
    return True

def user_id(review_id):
    sql = text("SELECT user_id FROM reviews WHERE id = :review_id")
    result = db.session.execute(sql, {"review_id":review_id})
    user = result.fetchone()
    return user

def get_reviews(movie_id):
    review_sql = text("SELECT * FROM reviews WHERE movie_id = :id")
    result = db.session.execute(review_sql, {'id': movie_id})
    movie_reviews = result.fetchall()
    return movie_reviews

def add_like(liketype, user_id, review_id):
    sql_update = text("INSERT INTO likes (liketype, user_id, review_id) VALUES (:liketype, :user_id, :review_id)")
    db.session.execute(sql_update, {'liketype': liketype, 'user_id': user_id, 'review_id': review_id})
    db.session.commit()
    return True

def likecount(review_id):
    sql = text("SELECT COUNT(*) FROM likes WHERE review_id = :review_id AND liketype ='like'")
    result = db.session.execute(sql, {'review_id': review_id})
    return result

def check_like(review_id, user_id):
    sql = text("SELECT 1 FROM likes WHERE review_id = :review_id AND user_id = :user_id")
    result = db.session.execute(sql, {'review_id':review_id, 'user_id': user_id})
    return result.fetchone()

def check_review(review_id):
    sql = text("SELECT * FROM reviews WHERE id = :review_id")
    result = db.session.execute(sql, {'review_id':review_id})
    return result.fetchone()
