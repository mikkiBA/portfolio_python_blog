from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, Email
import re

class SignUpForm(FlaskForm):
    user_name = StringField('ユーザー名', validators=[InputRequired(),
                       Length(max=255, message="255字以内で設定してください。")])

    password = StringField('パスワード')
    def validate_password(self, password):    
        if password.data == '':
             raise ValidationError("パスワードを入力してください。")
        
        if len(password.data) > 32:
             raise ValidationError("32文字以内で入力してください。")
        
        if len(password.data) < 8:
             raise ValidationError("8文字以上で入力してください。")
        
        if not re.search("[^a-zA-Z0-9_-]", password.data):
            return True
        else:
            raise ValidationError("半角英数字と_-のみ使用可能です。")

    email = StringField('メールアドレス', validators=[InputRequired(), 
                                               Length(max=255, message='255文字以内で入力してください。'), 
                                               Email()])

    age =  IntegerField('年齢', validators=[InputRequired()])

    submit = SubmitField('登録')



class UserAddForm(FlaskForm):
    user_name = StringField('ユーザー名', validators=[InputRequired(),
                       Length(max=255, message="255字以内で設定してください。")])

    furigana = StringField('ふりがな', validators=[Length(max=255, message='255文字以内で入力してください。')])

    password = StringField('パスワード')

    password = StringField('パスワード')
    def validate_password(self, password):    
        if password.data == '':
             raise ValidationError("パスワードを入力してください。")
        
        if len(password.data) > 32:
             raise ValidationError("32文字以内で入力してください。")
        
        if len(password.data) < 8:
             raise ValidationError("8文字以上で入力してください。")
        
        if not re.search("[^a-zA-Z0-9_-]", password.data):
            return True
        else:
            raise ValidationError("半角英数字と_-のみ使用可能です。")

    email = StringField('メールアドレス', validators=[InputRequired(), 
                                               Length(max=255, message='255文字以内で入力してください。'), 
                                               Email()])

    age =  IntegerField('年齢', validators=[InputRequired()])

    profile = StringField('プロフィール', validators=[Length(max=1500, message='1500文字以内で入力してください。')])

    submit = SubmitField('登録')



class EntryBody(FlaskForm):
    title = StringField('タイトル', validators=[InputRequired(),
                                                Length(min=1, max=60, message='80文字以内で入力してください。')])

    body = StringField('投稿内容', validators=[InputRequired(),
                                                Length(min=1, max=60, message='150文字以内で入力してください。')])
        
    submit = SubmitField('投稿')


class PasswordChangeForm(FlaskForm):
    password = StringField('パスワード')
    def validate_password(self, password):    
        if password.data == '':
             raise ValidationError("パスワードを入力してください。")
        
        if len(password.data) > 32:
             raise ValidationError("32文字以内で入力してください。")
        
        if len(password.data) < 8:
             raise ValidationError("8文字以上で入力してください。")
        
        if not re.search("[^a-zA-Z0-9_-]", password.data):
            return True
        else:
            raise ValidationError("半角英数字と_-のみ使用可能です。")
        
    submit = SubmitField('更新')


class EmailChangeForm(FlaskForm):
    email = StringField('更新メールアドレス', validators=[InputRequired(),
                                               Length(max=255, message='255文字以内で入力してください。'), 
                                               Email()])
        
    submit = SubmitField('更新')


class MypageChangeForm(FlaskForm):
    furigana = StringField('ふりがな', validators=[Length(max=255, message='255文字以内で入力してください。')])
    user_name = StringField('ユーザー名', validators=[Length(max=255, message='255文字以内で入力してください。')])
    profile = StringField('プロフィール', validators=[Length(max=1500, message='1500文字以内で入力してください。')])
    submit = SubmitField('更新')

class UserManagementForm(FlaskForm):
    furigana = StringField('ふりがな', validators=[Length(max=255, message='255文字以内で入力してください。')])
    user_name = StringField('ユーザー名', validators=[Length(max=255, message='255文字以内で入力してください。')])

    email = StringField('更新メールアドレス', validators=[InputRequired(),
                                               Length(max=255, message='255文字以内で入力してください。'), 
                                               Email()])

    password = StringField('パスワード')
    def validate_password(self, password):    
        if password.data == '':
             raise ValidationError("パスワードを入力してください。")
        
        if len(password.data) > 32:
             raise ValidationError("32文字以内で入力してください。")
        
        if len(password.data) < 8:
             raise ValidationError("8文字以上で入力してください。")
        
        if not re.search("[^a-zA-Z0-9_-]", password.data):
            return True
        else:
            raise ValidationError("半角英数字と_-のみ使用可能です。")  
    
    profile = StringField('プロフィール', validators=[Length(max=1500, message='1500文字以内で入力してください。')])
    submit = SubmitField('更新')


class ContentEditForm(FlaskForm):
    title = StringField('タイトル', validators=[Length(min=1, max=60, message='80文字以内で入力してください。')])

    body = StringField('投稿内容', validators=[Length(min=1, max=60, message='150文字以内で入力してください。')])
        
    submit = SubmitField('更新')   



class InquiryForm(FlaskForm):
    inquiry_title = StringField('お問い合わせ内容の要約', validators=[InputRequired(), 
                                                            Length(min=1, max=100, message='100文字以内で入力してください。')])

    inquiry_content = StringField('お問い合わせ内容詳細', validators=[InputRequired(), 
                                                            Length(min=1, max=300, message='300文字以内で入力してください。')])
        
    submit = SubmitField('送信')



class ReplyForm(FlaskForm):
    inquiry_reply = StringField('回答', validators=[InputRequired(), 
                                                            Length(min=1, max=1000, message='1000文字以内で入力してください。')])
        
    submit = SubmitField('返信')