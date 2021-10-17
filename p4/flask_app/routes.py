# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime

# local
from . import app, bcrypt, client
from .forms import (
    SearchForm,
    MovieReviewForm,
    RegistrationForm,
    LoginForm,
    UpdateUsernameForm,
    UpdateProfilePicForm,
)
from .models import User, Review, load_user
from .utils import get_b64_img, current_time

""" ************ View functions ************ """


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@app.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@app.route("/movies/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    form = MovieReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
            image=get_b64_img(current_user.picture),
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )


@app.route("/user/<username>")
def user_detail(username):
    u = User.objects(username=username).first()
    reviews = Review.objects(commenter=u)
    return render_template("user_detail.html", image=get_b64_img(current_user.picture), reviews=reviews)


@app.errorhandler(404)
def custom_404(e):
    return render_template("404.html"), 404


""" ************ User Management views ************ """


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("account"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, username=form.username.data, password=hashed_pwd)
        user.save()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("account"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is None:
            flash("Username does not exist!")
        elif not bcrypt.check_password_hash(user.password, form.password.data):
            flash("Username/Password incorrect!")
        else:
            login_user(user)
            return redirect(url_for("account"))

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    usernameUpdateForm = UpdateUsernameForm()
    if usernameUpdateForm.validate_on_submit():
        newUser = User.objects(username=usernameUpdateForm.username.data).first()

        if newUser is None:
            current_user.username = usernameUpdateForm.username.data
            current_user.save()
            # user.update(username=str(usernameUpdateForm.username.data))
            return redirect("account")

    profilePicUpdateForm = UpdateProfilePicForm()
    if profilePicUpdateForm.validate_on_submit():
        img = profilePicUpdateForm.picture.data
        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'

        if current_user.picture.get() is None:
            current_user.picture.put(img.stream, content_type=content_type)
        else:
            current_user.picture.replace(img.stream, content_type=content_type)
        current_user.save()
        return redirect("account")

    return render_template("account.html", usernameUpdateForm=usernameUpdateForm, profilePicUpdateForm=profilePicUpdateForm, image=get_b64_img(current_user.picture))
