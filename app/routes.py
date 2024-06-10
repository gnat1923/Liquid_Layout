from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Post

@app.route("/")
@app.route("/index")
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    
    return render_template("index.html", title="Liquid Layout Berlin", posts=posts)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.Select(User).where(User.username == form.username.data))
        if User is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        #flash("Login requested for user {}, remember me={}".format(form.username.data, form.remember_me.data))
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data,
                    body= form.body.data,
                    transit = form.transit.data,
                    neighbourhood = form.neighbourhood.data,
                    beer_rating = form.beer_rating.data,
                    guinness = form.guinness.data,
                    smoking = form.smoking.data,
                    music = form.music.data,
                    author = current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!")
        return redirect(url_for("index"))

    return render_template("post.html", title="Post", form=form)

@app.route("/posts/<id>")
def posts(id):
    post = Post.query.get_or_404(id)
    title = post.title
    return render_template("posts.html", title=title, post=post)