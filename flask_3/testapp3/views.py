from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager,login_user,logout_user,login_required, current_user
from sqlalchemy import desc
from .models.sns_db import db, User, Content, ContentGoodUser, Inquiry
from .models.form import EntryBody, ReplyForm, InquiryForm, EmailChangeForm, UserAddForm, PasswordChangeForm, UserManagementForm, SignUpForm, MypageChangeForm, ContentEditForm
#iインストールするのはPillowだがインポートするパッケージの名前はPillowではなくPILなので注意
from PIL import Image
from . import app
import os, random, string
from flask_wtf.csrf import CSRFProtect

#login manager起動、secret keyをセット
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'secret002'
csrf = CSRFProtect(app)

#認証ユーザーの呼び出し方を定義する
#userテーブルから指定のidを持つレコードを取り出す
@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


#indexページ、未ログインでも全ユーザーの投稿の閲覧が可能
#ログイン済みユーザーの場合、投稿一覧のうち、いいね済みの投稿はContentGoodUserを検索して、いいね済みならContentのgoodをTrueにする
@app.route("/")
def index():
    #いいね順に上から降順
    contents = Content.query.filter_by(deleted_flag=False).join(User).order_by(Content.good_count.desc()).all()
    if current_user.is_authenticated:
        user_auth = User.query.filter_by(id=current_user.id).first()
        #admin_flagの値によってhtml側の表示を変えたいため、ここで判断用の値を作る
        content_good_users = ContentGoodUser.query.filter_by(user_id=current_user.id).all()
        good_content = []
        for content_good_user in content_good_users:
            good_content.append(content_good_user.content.id)
        for content in contents:
            if content.id in good_content:
                content.good = True
        return render_template("index.html",contents=contents, user_auth=user_auth)
    #未ログイン時の'AnonymousUserMixin' object has no attribute 'id'のエラーを避けるため、user_auth=0を渡す
    return render_template("index.html",contents=contents, user_auth=0)


#ログイン画面
@app.route("/login")
def login():
    return render_template("login.html")


#ログインボタン押下後、DBに登録されているユーザー名・パスワードの組み合わせかどうかを判定
@app.route("/login_submit", methods=["POST"])
def login_submit():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    #ユーザーが存在しない場合、新規登録画面へ
    if user is None:
        return redirect(url_for("sign_up"))
    #ユーザーのアクセス拒否制限がオンの場合はエラー表示
    elif user.inaccessible == True:
        return render_template("inaccessible.html")
    else:
        password = request.form["password"]
        if password != user.password:
            return redirect(url_for("login"))        
        else:
            login_user(user)
            return redirect(url_for("index"))



#新規ユーザー登録、登録時のバリデーション
@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    signup_form = SignUpForm()
    if request.method == 'GET':
        return render_template("sign_up.html", signup_form=signup_form)

    if request.method == 'POST':
        user_name = request.form["user_name"]
        user = User.query.filter_by(user_name=user_name).first()
        if user is None:
            if signup_form.validate_on_submit():
                user_name = request.form["user_name"]
                password = request.form["password"]
                email = request.form["email"]
                gender = request.form['gender']
                age = request.form['age']
            
                new_user = User(user_name=user_name,
                            password=password,
                            email=email,
                            gender=gender,
                            age=age)
                
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)

                return redirect(url_for("index"))
        return render_template("sign_up.html", signup_form=signup_form)



#adminのuser管理 - 全ユーザー一覧
@app.route("/user_management")
@login_required
def user_management():
    general_users = User.query.filter_by(admin_flag=False, deleted_flag=False).order_by(User.id.asc()).all()
    admin_users = User.query.filter_by(admin_flag=True, deleted_flag=False).order_by(User.id.asc()).all()
    user_auth = User.query.filter_by(id=current_user.id).first()
    return render_template("user_management.html", general_users=general_users, admin_users=admin_users, user_auth=user_auth)



#adminのuser管理 - 新規ユーザー追加
@app.route("/user_management/user_add", methods=['GET', 'POST'])
@login_required
def user_add():
    useradd_form = UserAddForm()
    user_auth = User.query.filter_by(id=current_user.id).first()
    if user_auth.admin_flag == True:
        if request.method == 'GET':
            return render_template("user_add.html", useradd_form=useradd_form, user_auth=user_auth)

        if request.method == 'POST':
            user_email = request.form["email"]
            user = User.query.filter_by(email=user_email).first()
            if user is None:        
                if useradd_form.validate_on_submit():
                    user_name = request.form["user_name"]
                    furigana = request.form["furigana"]
                    password = request.form["password"]
                    email = request.form["email"]
                    age = request.form['age']
                    profile = request.form['profile']
                    gender = request.form['gender']

                    r_inaccessible = request.form['inaccessible']
                    r_admin_flag = request.form['admin_flag']

                    #ラジオボタンから受け取った値だと文字なのでここで型をboolへ戻す
                    if r_inaccessible == 'True':
                        inaccessible = True
                    else:
                        inaccessible = False
                    
                    #ラジオボタンから受け取った値だと文字なのでここで型をboolへ戻す
                    if r_admin_flag == 'True':
                        admin_flag = True
                    else:
                        admin_flag = False

                        

                        new_user = User(user_name=user_name,
                                        furigana=furigana,
                                        password=password,
                                        email=email,
                                        age=age,
                                        profile=profile,
                                        gender=gender,
                                        inaccessible=inaccessible,
                                        admin_flag=admin_flag)
                        
                        db.session.add(new_user)
                        db.session.commit()

                        return redirect(url_for("user_management"))
            return render_template("email_duplication.html")



#adminのuser管理 - ユーザー情報のedit
@app.route("/user_management/edit/<user_id>", methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    usermanagement_form = UserManagementForm()
    user = User.query.filter_by(id=user_id).first()
    user_auth = User.query.filter_by(id=current_user.id).first()
    if user_auth.admin_flag == True:
        if request.method == 'GET':
            return render_template("user_edit.html", usermanagement_form=usermanagement_form, user=user, user_auth=user_auth)
        
        if request.method == 'POST':
            if usermanagement_form.validate_on_submit():
                changed_user_name = request.form['user_name']
                changed_furigana = request.form['furigana']
                changed_email = request.form['email']
                changed_password = request.form['password']
                changed_profile = request.form['profile']

                gender = request.form['gender']
                inaccessible = request.form['inaccessible']

                #デフォルト値=変更なしなので、更新を行わない
                if not gender == 'default':
                    changed_gender = request.form['gender']
                    user.gender = changed_gender

                #ラジオボタンから受け取った値だと文字なのでここで型をboolへ戻す
                if not inaccessible == 'default':
                    if inaccessible == 'True':
                        changed_inaccessible = True
                    else:
                        changed_inaccessible = False
                    user.inaccessible = changed_inaccessible
                    
                user.user_name = changed_user_name
                user.furigana = changed_furigana
                user.email = changed_email
                user.password = changed_password
                user.profile = changed_profile

                db.session.commit()

                return redirect (url_for("user_management"))
            return render_template("user_edit.html", usermanagement_form=usermanagement_form, user=user, user_auth=user_auth)
    return render_template("error.html")



#adminのuser管理 - ユーザーのdelete
@app.route("/user_management/delete/<user_id>")
@login_required
def user_delete(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_auth = User.query.filter_by(id=current_user.id).first()
    if user_auth.admin_flag == True:
        user.deleted_flag = True
        db.session.commit()
        return render_template("user_management.html", user_auth=user_auth)
    return render_template("error.html")



#adminの投稿管理 - ユーザーの投稿一覧表示
@app.route("/content_management")
@login_required
def content_management():
    content_all = Content.query.filter_by(deleted_flag=False).join(User).all()
    user_auth = User.query.filter_by(id=current_user.id).first()
    return render_template("content_management.html", content_all=content_all, user_auth=user_auth)



#adminの投稿管理 - ユーザーの投稿編集
#adminの投稿管理 - ユーザーの投稿削除
#上記、2つの機能はuser側と同じルーティングにしている



#user側 - 新規投稿
@app.route("/entry", methods=['GET', 'POST'])
@login_required
def entry():
    entry_body = EntryBody()
    user_auth = User.query.filter_by(id=current_user.id).first()
    if request.method == 'GET':
        return render_template('entry.html', entry_body=entry_body, user_auth=user_auth)
    
    if request.method == 'POST':
        if entry_body.validate_on_submit():
            #user_idは現在ログインしているuser(cuurrent_user)をUserテーブルで検索してidを引っ張ってくる
            user_id = User.query.filter_by(user_name=current_user.user_name).first().id
            
            new_entry_title = request.form.get('title')
            new_entry_body = request.form.get('body')
       
            content = Content(
                title = new_entry_title,
                body = new_entry_body,
                user_id = user_id
            )

            db.session.add(content)
            db.session.commit()
            
            return redirect(url_for("mypage", user_name=current_user.user_name))
        
    title = '入力内容に誤りがあります'
    return render_template('entry.html', entry_body=entry_body, title=title, user_auth=user_auth)


#投稿の閲覧（ログイン不要でも見れる）
@app.route("/content/<content_id>")
def content(content_id):
    content = Content.query.filter_by(id=content_id, deleted_flag=False).join(User).first()
    user_auth = User.query.filter_by(id=current_user.id).first()
    #一つのidに対してのgood情報
    if current_user.is_authenticated:
        content_good_user = ContentGoodUser.query.filter_by(content_id=content_id, user_id=current_user.id).first()
        good_content = []
        if content_good_user is not None:
            good_content.append(content_good_user.content.id)
            #ContentテーブルのidがContentGoodUserテーブルと紐づくContentテーブルのidと同じならgood=True
        if content.id in good_content:
            content.good = True
        return render_template("content.html",content=content, user_auth=user_auth)
    return render_template("content.html",content=content, user_auth=0)



#ユーザーの投稿一覧（ログイン不要でも見れる）
@app.route("/user/<user_id>")
def user(user_id):
    user = User.query.filter_by(id=user_id).join(Content).all()[0]
    user_contents = Content.query.filter_by(user_id=user_id).join(User).order_by(Content.good_count.desc()).all()
    user_auth = User.query.filter_by(id=current_user.id).first()
    return render_template("user.html",user=user, user_contents=user_contents, user_auth=user_auth)



#user/admin - コンフィグ画面、表示
@app.route("/config")
@login_required
def config():
    user_config = User.query.filter_by(user_name=current_user.user_name).all()[0]
    user_auth = User.query.filter_by(id=current_user.id).first()
    return render_template("config.html", user_config=user_config, user_auth=user_auth)



#user/admin - コンフィグ画面、メールアドレスの更新
@app.route("/config/change_email", methods=["GET", "POST"])
@login_required
def config_change_email():
    emailchange_form = EmailChangeForm()
    user_auth = User.query.filter_by(id=current_user.id).first()
    if request.method == "GET":
        title = "登録メールアドレスを変更します"
        return render_template("config_change_email.html", emailchange_form=emailchange_form, title=title, user_auth=user_auth)

    if request.method == "POST":
        if emailchange_form.validate_on_submit():
            changed_email = request.form['email']

            user= User.query.filter_by(user_name=current_user.user_name).first()
            user.email = changed_email

            db.session.commit()

            title = "メールアドレスの変更が完了しました"
            return render_template("config_change_email.html", emailchange_form=emailchange_form, title=title, user_auth=user_auth)
        
    title = "入力に誤りがあります"
    return render_template("config_change_email.html", emailchange_form=emailchange_form, title=title, user_auth=user_auth)



#user/admin - コンフィグ画面、パスワードの更新
@app.route("/config/change_password", methods=["GET", "POST"])
@login_required
def config_change_password():
    passwordchange_form = PasswordChangeForm()
    user_auth = User.query.filter_by(id=current_user.id).first()
    if request.method == "GET":
        title = "パスワードを変更します"
        return render_template("config_change_password.html", passwordchange_form=passwordchange_form, title=title, user_auth=user_auth)

    if request.method == "POST":
        if passwordchange_form.validate_on_submit():
            changed_password = request.form['password']

            user= User.query.filter_by(user_name=current_user.user_name).first()
            user.password = changed_password

            db.session.commit()

            title = "パスワードの変更が完了しました"
            return render_template("config_change_password.html", passwordchange_form=passwordchange_form, title=title, user_auth=user_auth)
        
        title = "入力に誤りがあります"
        return render_template("config_change_password", passwordchange_form=passwordchange_form, title=title, user_auth=user_auth)



#マイページ、自分の投稿した記事一覧が表示される
@app.route("/mypage")
@login_required
def mypage():
    user= User.query.filter_by(user_name=current_user.user_name).first()
    user_auth = User.query.filter_by(id=current_user.id).first()
    #Contentsのuser_idを引っ張ってくるために、外部キーであるUserのid(user.id)を使う
    contents = Content.query.filter_by(user_id=current_user.id, deleted_flag=False).join(User).order_by(Content.good_count.desc()).all()
    return render_template("mypage.html", contents=contents, user=user, user_auth=user_auth)



#マイページ、登録情報の変更① - ふりがな、ユーザー名、プロフィール欄
@app.route("/mypage/change_profile", methods=['GET', 'POST'])
@login_required
def mypage_change_profile():
    mypagechange_form = MypageChangeForm()
    user= User.query.filter_by(user_name=current_user.user_name).first()
    user_auth = User.query.filter_by(id=current_user.id).first()
    if request.method == 'GET':
        title = "現在の登録内容を表示しています。変更が必要な欄のみ入力してください"
        return render_template("mypage_change_profile.html", mypagechange_form=mypagechange_form, user=user, title=title, user_auth=user_auth)
    
    if request.method == 'POST':
        if mypagechange_form.validate_on_submit():
            changed_furigana = request.form['furigana']
            changed_user_name = request.form['user_name']
            changed_profile = request.form['profile']

            user.furigana = changed_furigana
            user.user_name = changed_user_name
            user.profile = changed_profile
            db.session.commit()

            title = "マイページ情報の更新が変更が完了しました"
            return render_template("mypage_change_profile.html", mypagechange_form=mypagechange_form, user=user, title=title, user_auth=user_auth)
        
        title = "入力に誤りがあります"
        return render_template("mypage_change_profile.html", mypagechange_form=mypagechange_form, title=title, user_auth=user_auth)



#マイページ、登録情報の変更② - アイコン画像
    
#ここで2mbを超えるサイズの画像はアップロードできないと定義
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

@app.route("/mypage/icon_upload", methods=['GET', 'POST'])
@login_required
def mypage_icon_upload():
    user = User.query.filter_by(id=current_user.id).all()[0]
    user_auth = User.query.filter_by(id=current_user.id).first()
    if request.method == 'GET':
        return render_template('mypage_icon_upload.html', user=user, user_auth=user_auth)

    if request.method == 'POST':
        if 'icon' not in request.files:
            flash("画像ファイルが添付されていません")
            return redirect(url_for('mypage_icon_upload'))
        
        icon = request.files["icon"]
        if icon.filename == '':
            flash("画像ファイルが添付されていません")
            return redirect(url_for('mypage_icon_upload'))
        
        else:
            #filename.jpg / filename.png以外は受け付けない
            file_extension = icon.filename.rsplit('.', 1)[1]
            if file_extension in ["jpg", "png"]:
                #iconファイル名の変更
                icon = Image.open(request.files['icon'])
                old_icon_name = user.icon_file_name
                new_icon_name = ''.join(random.choices(string.ascii_letters+string.digits,k=10))+".jpg"
                user.icon_file_name = new_icon_name
                db.session.commit()

                #pngファイルのままだとエラーが起きる場合があるので、jpgへ変換する
                resized_icon = icon.resize((256, 256)).convert('RGB')
                resized_icon.save("testapp3/static/uploads/"+new_icon_name)
                if (old_icon_name != 'default_icon.jpg') and os.path.exists("testapp3/static/uploads/"+old_icon_name):
                    os.remove("testapp3/static/uploads/"+old_icon_name)
                return redirect(url_for('mypage'))
            else:
                abort(404)
    return redirect(url_for('mypage_icon_upload'))



#投稿編集
@app.route("/content_management/edit/<content_id>", methods=['GET', 'POST'])
@app.route("/mypage/content_edit/<content_id>", methods=['GET', 'POST'])
@login_required
def content_edit(content_id):
    contentedit_form = ContentEditForm()
    content = Content.query.filter_by(id=content_id).join(User).all()[0]
    user_auth = User.query.filter_by(id=current_user.id).first()
    if request.method == 'GET':
        return render_template("content_edit.html", contentedit_form=contentedit_form, content_id=content_id, content=content, user_auth=user_auth)
    
    if request.method == 'POST':
        if contentedit_form.validate_on_submit:
            edited_title = request.form.get('title')
            edited_body = request.form.get('body')

            #投稿者本人かadmin以外は編集できない
            if current_user.id == content.user_id or current_user.admin_flag == True:

                content.title = edited_title
                content.body = edited_body

                db.session.commit()

                if current_user.id == content.user_id:
                    return redirect(url_for('mypage'))
                if current_user.admin_flag == True:
                    return redirect(url_for('content_management'))
                
            return render_template("error.html")
        
        return render_template("content_edit.html")


#投稿削除
@app.route("/admin/content_delete/<content_id>", methods=['GET'])
@app.route('/mypage/content_delete/<content_id>', methods=['GET'])
@login_required
def content_delete(content_id):
    content = Content.query.filter_by(id=content_id).join(User).all()[0]
    if current_user.id == content.user_id or current_user.admin_flag == True:
        #論理削除
        content.deleted_flag = True
        db.session.commit()

        if current_user.admin_flag == True:
            return redirect("content_management")
        else:
            return redirect(url_for("mypage"))
        
    return render_template("error.html")



#問い合わせ - user側
@app.route("/inquiry", methods=['GET','POST'])
@login_required
def inquiry():
    inquiry_form = InquiryForm()
    user = User.query.filter_by(id=current_user.id).first()
    user_inquiries = Inquiry.query.filter_by(user_id=user.id).all()
    user_auth = User.query.filter_by(id=current_user.id).first()
    if request.method == 'GET':
        return render_template('inquiry.html', inquiry_form=inquiry_form, user_inquiries=user_inquiries, user_auth=user_auth)

    if request.method == 'POST':
        if inquiry_form.validate_on_submit:
            new_inquiry_title = request.form['inquiry_title']
            new_inquiry_content = request.form['inquiry_content']

        if current_user.id == user.id:
            new_inquiry = Inquiry(inquiry_title=new_inquiry_title,
                                  inquiry_content=new_inquiry_content,
                                  user_id = user.id)

            db.session.add(new_inquiry)
            db.session.commit()

            return redirect(url_for('inquiry'))
        return redirect(url_for('inquiry'))



#問い合わせ - admin側
@app.route("/inquiry_management", methods=['GET'])
@login_required
def inquiry_management():
    new_inquiries = Inquiry.query.filter_by(status='受付').join(User).all()
    replied_inquiries = Inquiry.query.filter_by(status='回答済').join(User).all()
    user_auth = User.query.filter_by(id=current_user.id).first()
    return render_template('inquiry_management.html', new_inquiries=new_inquiries, replied_inquiries=replied_inquiries, user_auth=user_auth)

@app.route("/inquiry_management/<inquiry_id>", methods=['GET','POST'])
@login_required
def inquiry_reply(inquiry_id):
    reply_form = ReplyForm()
    user_inquiry = Inquiry.query.filter_by(id=inquiry_id).join(User).all()[0]
    user_auth = User.query.filter_by(id=current_user.id).first()
    if request.method == 'GET':
        title = "問い合わせに対する回答を入力してください"
        return render_template('inquiry_reply.html', reply_form=reply_form, user_inquiry=user_inquiry, title=title, user_auth=user_auth)

    if request.method == 'POST':
        if reply_form.validate_on_submit:
            new_inquiry_reply = request.form['inquiry_reply']
            
        if current_user.admin_flag == True:

            user_inquiry.inquiry_reply = new_inquiry_reply
            user_inquiry.status = "回答済"
            db.session.commit()

            return redirect(url_for('inquiry_management'))
        title = "入力内容に誤りがあります"
        return render_template('inquiry_management.html',reply_form=reply_form, title=title, user_auth=user_auth)
    



#いいねボタン
@app.route("/good", methods=["POST"])
@login_required
def good():
    content_id = request.json['content_id']
    content = Content.query.filter_by(id=content_id).all()[0]
    user_id = current_user.id
    content_good_user = ContentGoodUser.query.filter_by(content_id=content_id,user_id=user_id).all()
    if len(content_good_user) >= 1:
        db.session.delete(content_good_user[0])
        content.good_count = content.good_count - 1
    else:
        content_good_user = ContentGoodUser(content_id=content_id,user_id=user_id)
        db.session.add(content_good_user)
        content.good_count = content.good_count + 1
    db.session.commit()
    return str(content.good_count)



#ログアウトボタン
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))