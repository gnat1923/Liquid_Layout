from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, PostForm, neighbourhoods_list, transit_list
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Post

'''@app.route("/")
@app.route("/index")
def index():
    posts = Post.query.filter_by(visible=True).order_by(Post.timestamp.desc()).all()
    
    return render_template("index.html", title="Liquid Layout Berlin", posts=posts)'''

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!")
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
    flash("Log out successful")
    return redirect(url_for("index"))

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        file_data = None
        if form.image_data.data:
            file = form.image_data.data
            if file.filename != "":
                file_data = file.read()


        post = Post(title = form.title.data,
                       body = form.body.data,
                       map_embed = form.map_embed.data,
                       transit = form.transit.data,
                       neighbourhood = form.neighbourhood.data,
                       beer_rating = form.beer_rating.data,
                       guinness= form.guinness.data,
                       smoking = form.smoking.data,
                       music = form.music.data,
                       visible = form.visible.data,
                       image_data=file_data,
                        image_filename=file.filename if file_data else None,
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
    form = PostForm()
    return render_template("posts.html", title=title, post=post, form=form)

@app.route("/posts/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    
    
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    title = f"Edit post {post.title}"

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.map_embed = form.map_embed.data
        post.transit = form.transit.data
        post.neighbourhood = form.neighbourhood.data
        post.beer_rating = form.beer_rating.data
        post.guinness= form.guinness.data
        post.smoking = form.smoking.data
        post.music = form.music.data
        post.visible = form.visible.data
        
        post.author = current_user

        if form.image_data.data:
            post.image_data = form.image_data.data.read()
            post.image_filename = form.image_filename.data
        else:
            post.image_data = None
            post.image_filename = None

        db.session.commit()
        flash("Post updated successfully!")
        dynamic_url = url_for("posts", id=post.id)
        return redirect(dynamic_url)
    
    return render_template("edit_post.html", title=title, post=post, form=form)

@app.route('/toggle_visibility/<int:post_id>', methods=['POST'])
@login_required
def toggle_visibility(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        flash('You do not have permission to edit this post.', 'danger')
        return redirect(url_for('edit_post', post_id=post_id))
    post.visible = not post.visible
    db.session.commit()
    flash('Post visibility updated.', 'success')

    return redirect(url_for('posts', id=post_id))

@app.route("/delete_post/<id>", methods=["POST"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post has been deleted", "success")
    return redirect(url_for("index"))

@app.route("/all_posts", methods=["GET"])
@login_required
def show_all_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template("show_all_posts.html", posts=posts)

@app.route("/index", methods=["POST","GET"])
def index():
    # Get filter values from the request
    neighbourhood = request.args.get('neighbourhood')
    smoking = request.args.get('smoking')
    guinness = request.args.get('guinness')

    # Start with all posts
    posts_query = Post.query

    # Apply filters
    if neighbourhood:
        posts_query = posts_query.filter(Post.neighbourhood == neighbourhood)
    if smoking:
        smoking_bool = smoking.lower() == 'true'
        posts_query = posts_query.filter(Post.smoking == smoking_bool)
    if guinness:
        guinness_bool = guinness.lower() == 'true'
        posts_query = posts_query.filter(Post.guinness == guinness_bool)

    # Get the filtered posts
    posts = posts_query.order_by(Post.timestamp.desc()).all()

    return render_template('filter_index.html', posts=posts, neighbourhoods_list=neighbourhoods_list)