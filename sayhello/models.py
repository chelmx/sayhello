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
    root_id = db.Column(db.Integer, db.ForeignKey('message.id'))

    user = db.relationship('User', back_populates='messages')
    replies = db.relationship('Message', back_populates='replied', foreign_keys=[replied_id], cascade='all, delete-orphan')
    replied = db.relationship('Message', back_populates='replies', foreign_keys=[replied_id], remote_side=[id])
    messages = db.relationship(
        'Message',                          # 关联自身模型（自引用）
        primaryjoin='Message.root_id == Message.id',  # 核心条件：子孙的 root_id = 当前消息的 id
        foreign_keys='Message.root_id',     # 子孙节点的 root_id 字段作为外键
        viewonly=True,                      # 只读（派生关系，无需SQLAlchemy自动维护）
        lazy='dynamic',                     # 延迟加载（返回Query对象，可进一步过滤）
        back_populates=None                 # 无需反向引用（派生关系）
    )