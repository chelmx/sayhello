# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, flash, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user, login_required

from sqlalchemy import or_

from sayhello import app, db
from sayhello.forms import LoginForm, HelloForm
from sayhello.models import User, Message

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user:
            if username == user.username and user.validate_password(password):
                login_user(user, remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()

@app.route('/', methods=['GET'])
def index():
    reply = request.args.get('reply')
    if reply:
        reply = Message.query.get_or_404(reply)
    form = HelloForm()
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.filter(or_(Message.reviewed == True, hasattr(current_user, 'id') and Message.user_id == current_user.id)).order_by(Message.timestamp.desc()).paginate(page, per_page=10)
    args_except_reply = {k: v for k, v in request.args.items() if k != 'reply'}
    return render_template('index.html', reply=reply, form=form, pagination=pagination, args_except_reply=args_except_reply)

@app.route('/', methods=['POST'])
@login_required
def index_post():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        color = form.color.data
        body = form.body.data
        message = Message(body=body, color=color, name=name, user=current_user)
        reply = request.args.get('reply')
        if reply:
            message.replied = Message.query.get_or_404(reply)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
    return redirect(url_for('index'))
