from app import app
import users
import reviews
from db import db
from flask import Flask
from flask import redirect, render_template, request, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from os import getenv



@app.route("/")
def index():
    result = db.session.execute(text("SELECT * FROM movies"))
    movies = result.fetchall()
    return render_template("index.html", count=len(movies), movies=movies)


@app.route('/movie/<string:title>')
def movie_detail(title):
    sql = text("SELECT * FROM movies WHERE name = :title")
    result = db.session.execute(sql, {'title': title})
    movie = result.fetchone()

    review_sql = text("SELECT * FROM reviews WHERE movie_id = :id")
    result2 = db.session.execute(review_sql, {'id': movie[0]})
    movie_reviews = result2.fetchall()

    user_sql = text("SELECT * FROM users WHERE id = :id")
    users = []
    timestamps = []
    scores = []
    likecounts = []
    for review in movie_reviews:

        user_result = db.session.execute(user_sql, {'id':review[3]})
        user = user_result.fetchone()
        users.append(user[1])

        like_sql = text("SELECT COUNT(*) FROM likes WHERE review_id = :review_id AND liketype ='like'")
        like_result = db.session.execute(like_sql, {'review_id': review.id})
        likecounts.append(like_result.scalar())
        timestamps.append(str(review[5])[:16])
        scores.append(review[2])

    if len(scores) == 0:
        score = 0
    else:
        scoretemp = float(sum(scores)/len(scores))
        score = f"{scoretemp:.2f}"

    for timestamp in timestamps:
        timestamp = str(timestamp)[:16]

    if movie:
        return render_template('movie_detail.html', movie=movie,movie_reviews=movie_reviews, timestamps=timestamps, users=users, score=score, likecounts=likecounts)
    else:
        return render_template("error.html", message = "Something went wrong")
    
@app.route('/movie/<string:title>/review', methods=['GET','POST'])
def review(title):
    sql = text("SELECT * FROM movies WHERE name = :title")
    result = db.session.execute(sql, {'title':title})
    movie = result.fetchone()
    if not movie:
        return render_template("error.html", message = "Movie doesn't exist")
    if request.method == "POST":
        score = int(request.form["score"])
        content = request.form["review_text"]
        if session["username"]:
            username = session["username"]
        else:
            return render_template("error.html", message="Review failed")
        if reviews.review(score, content, username, movie):
            return redirect("/")
        else:
            return render_template("error.html", message="Review failed")


    return render_template('review.html',movie=movie)

@app.route('/like-review/<int:review_id>', methods=['POST'])
def like_review(review_id):
    action = request.form.get('action')
    username = session["username"]
    user_id = users.user_id(username)
    like_sql = text("SELECT 1 FROM likes WHERE review_id = :review_id AND user_id = :user_id")
    likeresult = db.session.execute(like_sql, {'review_id':review_id, 'user_id': user_id})

    if likeresult.fetchone():
        return render_template("error.html", message = "Already liked or disliked")

    sql = text("SELECT * FROM reviews WHERE id = :review_id")
    result = db.session.execute(sql, {'review_id':review_id})
    review = result.fetchone()

    if not review:
        return render_template("error.html", message = "Review doesn't exist")


    sql_update = text("INSERT INTO likes (liketype, user_id, review_id) VALUES (:action, :user_id, :review_id)")
    db.session.execute(sql_update, {'action': action, 'user_id': user_id, 'review_id': review_id})
    db.session.commit()

    return redirect("/")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message = "Wrong username or password")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Different passwords entered")
        if users.register(username, password1):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed")
