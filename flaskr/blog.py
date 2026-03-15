from flask import (
    Blueprint, redirect, render_template, url_for
)
from werkzeug.exceptions import abort
from flask_login import login_required, current_user

from .extensions import db
from .models import Post
from .forms import PostForm

bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template("blog/index.html", posts=posts)

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("blog.index"))
    
    return render_template("blog/create.html", form=form)

def get_post(id, check_author=True):
    post = Post.query.get(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    
    if check_author and post.author_id != current_user.id:
        abort(403)
    
    return post

@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for("blog.index"))
    
    return render_template("blog/update.html", post=post, form=form)

@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("blog.index"))