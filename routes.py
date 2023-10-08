from app import app
import users
import reviews
import movies as sqlmovies
from db import db
from flask import Flask
from flask import redirect, render_template, request, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from os import getenv



@app.route("/")
def index():
    movies = sqlmovies.get_movies()
    return render_template("index.html", count=len(movies), movies=movies)


@app.route('/movie/<string:title>')
def movie_detail(title):
    movie = sqlmovies.movie_name(title)
    movie_reviews = reviews.get_reviews(movie[0])
    movie_genres = sqlmovies.movie_genres(movie[0])

    userslist = []
    timestamps = []
    likecounts = []
    dislikecounts = []
    for review in movie_reviews:

        user = users.get_user_by_id(review[3])
        userslist.append(user[1])

        likecount = reviews.likecount(review.id)
        dislikecount = reviews.dislikecount(review.id)
        likecounts.append(likecount.scalar())
        dislikecounts.append(dislikecount.scalar())

        timestamps.append(str(review[5])[:16])

    scoretemp = sqlmovies.avg_score(movie.id)
    
    if not scoretemp:
        score = 0
    else:
        score = f"{scoretemp:.2f}"

    if movie:
        return render_template('movie_detail.html', 
                               movie=movie,
                               movie_reviews=movie_reviews, 
                               movie_genres=movie_genres,
                               timestamps=timestamps, 
                               users=userslist, 
                               score=score, 
                               likecounts=likecounts,
                               dislikecounts=dislikecounts 
                               )
    else:
        return render_template("error.html", message = "Something went wrong")
  
@app.route('/movie/<string:title>/review', methods=['GET','POST'])
def review(title):
    movie = sqlmovies.movie_name(title)

    if not movie:
        return render_template("error.html", message = "Movie doesn't exist")
    if request.method == "POST":
        score = int(request.form["score"])
        content = request.form["review_text"]
        if session["username"]:
            username = session["username"]
        else:
            return render_template("error.html", message="Review failed, not logged in or username doesn't exist")
        if reviews.review(score, content, username, movie):
            movies = sqlmovies.get_movies()
            return render_template('index.html', message = f"Review left successfully", count=len(movies), movies=movies)
        else:
            return render_template("error.html", message="Review failed, you have already reviewed the movie")


    return render_template('review.html',movie=movie)

@app.route('/like-review/<int:review_id>', methods=['POST'])
def like_review(review_id):
    action = request.form.get('action')
    if action == "like" or "dislike":
        username = session["username"]
        user_id = users.user_id(username)

        like_check = reviews.check_like(review_id, user_id)

        if like_check:
            return render_template("error.html", message = "Already liked or disliked")
        
        review = reviews.check_review(review_id)

        if not review:
            return render_template("error.html", message = "Review doesn't exist")

        reviews.add_like(action, user_id, review_id)

    movies = sqlmovies.get_movies()
    return render_template('index.html', message = f"Review {action}d successfully", count=len(movies), movies=movies)

@app.route('/confirm-delete-review/<int:review_id>', methods=['POST'])
def confirm_delete_review(review_id):
    user_id = reviews.user_id(review_id)
    print(user_id[0])
    if not session["is_admin"] and session["user_id"] != user_id[0]:
        return render_template("error.html", message = "You do not have permission to delete reviews")

    review = review_id

    if not review:
        return render_template("error.html", message = "Review doesn't exist")

    return render_template('confirm_delete_review.html', review=review)


@app.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    movies = sqlmovies.get_movies()
    confirm = request.form.get('confirm')
    if confirm == "yes":
        review_id = review_id
        reviews.delete_review(review_id)
        return render_template('index.html', message = "Review deleted successfully", count=len(movies), movies=movies)
    return render_template('index.html', message = "Review not deleted", count=len(movies), movies=movies)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            user_id = users.user_id(username)
            session["user_id"] = user_id
            session["username"] = username
            session["is_admin"] = users.is_admin(username)
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
        is_admin = request.form["admin"]
        if len(username) < 3:
            return render_template("error.html", message="Username must be 3 characters or longer")
        if password1 != password2:
            return render_template("error.html", message="Different passwords entered")
        if users.register(username, password1, is_admin):
            user_id = users.user_id(username)
            session["user_id"] = user_id
            session["username"] = username
            session["is_admin"] = users.is_admin(username)
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed")

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if not session["is_admin"]:
        return render_template("error.html", message = "You do not have permission to this page")
    movies = sqlmovies.get_movies()
    genres = sqlmovies.get_genres()
    return render_template('admin.html', movies = movies, genres = genres)

@app.route('/add-movie', methods=['POST'])
def add_movie():
    if not session["is_admin"]:
        return render_template("error.html", message = "You do not have permission to this page")

    movie_name = request.form['movie_name']
    movie_year = request.form['year']
    

    sqlmovies.add_movie(movie_name, movie_year)
    movies = sqlmovies.get_movies()
    genres = sqlmovies.get_genres()
    return render_template("admin.html", message =f" Movie: {movie_name}, {movie_year} added successfully.", movies = movies, genres = genres)

@app.route('/add-genre', methods=['POST'])
def add_genre():
    if not session["is_admin"]:
        return render_template("error.html", message = "You do not have permission to this page")

    genre_name = request.form['genre_name']

    sqlmovies.add_genre(genre_name)
    movies = sqlmovies.get_movies()
    genres = sqlmovies.get_genres()
    return render_template("admin.html", message =f" Genre {genre_name} added successfully.", movies = movies, genres = genres)


@app.route('/link-genre', methods=['POST'])
def link_genre():
    if not session["is_admin"]:
        return render_template("error.html", message = "You do not have permission to this page")

    movie = request.form['movie_id']
    genre = request.form['genre_id']

    sqlmovies.link_genre(movie, genre)
    movies = sqlmovies.get_movies()
    genres = sqlmovies.get_genres()
    return render_template("admin.html", message =f" Genre linked to movie successfully.", movies = movies, genres = genres) 
