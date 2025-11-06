# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from sayhello import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    messages = db.relationship('Message', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    color = db.Column(db.String(7))
    body = db.Column(db.String(200))
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('message.id'))

    user = db.relationship('User', back_populates='messages')
    replies = db.relationship('Message', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Message', back_populates='replies', remote_side=[id])