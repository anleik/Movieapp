from db import db
from flask import session
from sqlalchemy.sql import text




def review(score, content, username, movie):
    check_username_sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(check_username_sql, {"username":username})
    user = result.fetchone()

    if not user:
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
