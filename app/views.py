from flask import render_template, flash, redirect, session, url_for, request, g
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, current_user
from flask_login import logout_user, login_required
from app import app, db
from .models import User, Post
from .forms import LoginForm, RegistrationForm, EditForm, PostForm, EditPostForm, CommentForm, EditPasswordForm


@app.route("/")
def homepage():
    app.logger.info('Welcome')
    return render_template('index.html',
                           title='Homepage')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('homepage')
            return redirect(next)
        flash('Invalide username or password.')
    app.logger.info('Logged in')
    return render_template('login.html',
                           title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You could login now !')
        return redirect(url_for('homepage'))
    return render_template('register.html',
                           title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    app.logger.info('logout')
    flash('You have been logged out')
    return redirect(url_for('homepage'))


@app.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    app.logger.info('User')
    return render_template('user.html', user=user)


@app.route('/edit_my/<name>', methods=['GET', 'POST'])
def edit_my(name):
    user = User.query.filter_by(name=name).first_or_404()
    form = EditForm(obj=user)
    if form.validate_on_submit():
        user.about = form.about.data
        user.location = form.location.data
        user.name = form.name.data
        user.birth = form.birth.data
        db.session.commit()
        flash('Your profile has been updated.')
        app.logger.info('Edited name')
        return redirect('/')
    return render_template('edit_my.html',
                           title='Edit Profile',
                           form=form)


@app.route('/comment_post/<id>', methods=['GET', 'POST'])
def comment_post(id):
    post = Post.query.get(id)
    form = CommentForm(obj=post)
    if form.validate_on_submit():
        post.comment = form.comment.data
        db.session.commit()
        app.logger.info('posted')
        return redirect('/forum')
    return render_template('comment_post.html',
                           title='Edit Post',
                           form=form)


@app.route('/edit_password/<name>', methods=['GET', 'POST'])
def edit_password(name):
    #user = User.query.filter_by(name=name).first_or_404()
    form = EditPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your password has been updated.')
        app.logger.info('password has been updated')
        return redirect('/')
    return render_template('edit_password.html',
                           title='Edit Password',
                           form=form)


@app.route('/edit_post/<id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get(id)
    form = EditPostForm(obj=post)
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.commit()
        app.logger.info('edited post')
        return redirect('/forum')
    return render_template('edit_post.html',
                           title='Edit Post',
                           form=form)


@app.route('/delete_post/<id>', methods=['GET'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    app.logger.info('post deleted')
    db.session.commit()
    return redirect('/forum')


@app.route('/explore', methods=['GET'])
def get_all():
    users = []
    user = User.query.all()
    for i in user:
        if i.name != current_user.name:
            users.append(i)
    app.logger.info('user list')
    return render_template('explore.html',
                           title='All User',
                           users=users)


@app.route('/explore_detail/<id>', methods=['GET'])
def get_detail(id):
    user = User.query.filter_by(id=id).first_or_404()
    app.logger.info('user homepage')
    return render_template('explore_detail.html',
                           title='All User',
                           user=user)


@app.route('/forum', methods=['GET', 'POST'])
def forum():
    user = User.query.all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user.name)
        db.session.add(post)
        db.session.commit()
        app.logger.info('forum')
        return redirect(url_for('forum'))
    posts = Post.query.all()
    return render_template('forum.html', form=form, posts=posts, user=user)


@app.route('/blog_user/<name>')
def blog_user(name):
    user = User.query.filter_by(name=name).first_or_404()
    app.logger.info('user')
    return render_template('blog_user.html', user=user)

# @app.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.ping()
#         if not current_user.confirmed \
#                 and request.endpoint \
#                 and request.blueprint != 'app' \
#                 and request.endpoint != 'static':
#             return redirect(url_for('app.unconfirmed'))
