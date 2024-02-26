from testapp3 import db
from datetime import datetime
from flask_login import UserMixin


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    good_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時
    deleted_flag = db.Column(db.Boolean, nullable=False, default=False) #削除したか否かのフラグ、trueなら削除したことを示す
    #リレーション: backrefで双方向
    user = db.relationship('User', backref='content')
    #いいね済みかどうかを保持
    good = False

    def __repr__(self):
        return '<Content %r>' % self.title



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    furigana = db.Column(db.String(255), default='')
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    profile = db.Column(db.String(1500), default='')
    icon_file_name = db.Column(db.String(255), default='default_icon.jpg') #プロフィール画像のファイル名
    admin_flag = db.Column(db.Boolean, nullable=False, default=False) #一般userとAdminのフラグ、trueならadminであることを示す
    inaccessible = db.Column(db.Boolean, nullable=False, default=False) #アクセス可否、Trueならアクセス拒否
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時
    deleted_flag = db.Column(db.Boolean, nullable=False, default=False) #削除したか否かのフラグ、trueなら削除したことを示す

    def __repr__(self):
        return '<User %r>' % self.name



class ContentGoodUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    #リレーション: backrefで双方向
    content = db.relationship('Content', backref='content_good_user')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #リレーション: backrefで双方向
    user = db.relationship('User', backref='content_good_user')


class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inquiry_title = db.Column(db.String(80), nullable=False)
    inquiry_content = db.Column(db.Text, nullable=False)
    inquiry_reply = db.Column(db.Text, nullable=False, default='回答待ち')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=0) #問い合わせの優先度、default:0, 1:high, 2:middle, 3:low
    status = db.Column(db.String(10), nullable=False, default='受付')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時
    user = db.relationship('User', backref='inquiry')

    def __repr__(self):
        return '<Inquiry %r>' % self.name

