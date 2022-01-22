from fileinput import filename
from typing import Final
from flask import (current_app, render_template, 
                    redirect, 
                    url_for,
                    request, 
                    flash,
                    abort)
from FlaskBlogApp.forms import NewArticleForm, SignupForm, LoginForm, NewArticleForm, AccountUpdateForm
from FlaskBlogApp import app, db, bcrypt
from FlaskBlogApp.models import User, Article

from flask_login import login_user, logout_user, current_user, login_required
import secrets, os
from PIL import Image


def image_save(image, where, size): #size is a tuple (width, height)
    random_filename = secrets.token_hex(12)
    image_extension = os.path.splitext(image.filename)[1]
    
    image_filename = random_filename + image_extension

    try:
        image_path = os.path.join(app.root_path, 'static/images/', where, image_filename)
    except:
        abort(415)

    img = Image.open(image)
    img.thumbnail(size)
    img.save(image_path)

    return image_filename

@app.route('/index')
@app.route('/')
def root():
    articles = Article.query.order_by(Article.date_created.desc())
    return  render_template('index.html', articles=articles)


@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('root'))

    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        encrypted_password= bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=encrypted_password)
        db.session.add(user)
        db.session.commit()

        flash(f"O λογαρισμός για τον χρήστη <b>{username}</b> δημιουργήθηκε με επιτυχία ", "success")

        return redirect(url_for('login'))
    else:
        pass
    return render_template('signup.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('root'))

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            
            login_user(user, remember=form.remember_me.data)
            next_link = request.args.get('next')

            flash(f"Η είσοδος του χρήστη με email: {email} είναι επιτυχής", "success")
            if next_link:
                return redirect(next_link)
            return redirect(url_for('root'))
        else:
            flash(f"H σύνδεση παρακαλώ δοκιμάστε ξανά", "danger")
        print(email, password)

        

    return render_template('login.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    flash(f"Έγινε αποσύνδεση", "success")
    return redirect(url_for('root'))

@app.route('/new_article/', methods=['GET', 'POST'])
@login_required
def new_article():

    form = NewArticleForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        
        if form.article_image.data:
            try:
                image_file = image_save(form.article_image.data, 'article_images', (640, 360))
            except:
                abort(415)

            article = Article(article_title=form.article_title.data, article_body=form.article_body.data, author=current_user, article_image=image_file)
        else:
            article = Article(article_title=form.article_title.data, article_body=form.article_body.data, author=current_user)

        db.session.add(article)
        db.session.commit()
        flash(f"O χρήστης <b>{current_user.username}</b> προσθεσε ενα άρθρο με επιτυχία","success")
        return redirect(url_for('root'))

    return render_template('new_article.html', form=form, page_title="Νέο Άρθρο")


@app.route('/full_article/<int:article_id>')
def full_article(article_id):

    article = Article.query.get_or_404(article_id)
    return render_template('full_article.html', article=article)



@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):

    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()

    form = NewArticleForm(article_title=article.article_title, article_body=article.article_body)

    if request.method == 'POST' and form.validate_on_submit():
        article.article_title = form.article_title.data
        article.article_body = form.article_body.data

        if form.article_image.data:

            if article.article_image!='default_article_image.jpg':

                try:
                    os.remove(os.path.join(app.root_path, 'static/images/article_images',article.article_image))
                except FileNotFoundError:
                    pass

            try:
                image_file = image_save(form.article_image.data, 'article_images', (640, 360))
            except:
                abort(415)

            article.article_image=image_file



        db.session.commit()

        flash(f"Το άρθρο με τίτλο {article.article_title} επεξεργάστηκε  με επιτυχία", "success")
        return redirect(url_for('root'))

    return render_template('new_article.html', form=form, page_title="Eπεξεργασία Άρθρου")


@app.route('/delete_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def delete_article(article_id):

    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()

    if not article:
        flash(flash(f"To άρθρο δεν βρέθηκε","danger"))
    else:
        db.session.delete(article)
        db.session.commit()
        flash(f"To άρθρο με τίτλο <b>{article.article_title}</b> διαγράφτηκε","success")
    
    return redirect(url_for('root'))





@app.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():

    form = AccountUpdateForm(username=current_user.username, email=current_user.email)

    if request.method == 'POST' and form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data
        
        if form.profile_image.data:
            
            if current_user.profile_image!='default_profile_image.jpg':
                try:
                    os.remove(os.path.join(app.root_path, 'static/images/profile_images', current_user.profile_image))
                except FileNotFoundError:
                    pass

            try:
                image_file = image_save(form.profile_image.data, 'profile_images', (240, 240))
            except:
                abort(415)

            current_user.profile_image = image_file

        db.session.commit()
        flash(f"Η ενημέρωση των στοιχείων του χρήστη <b>{current_user.username}</b> έγινε με επιτυχία","success")
        return redirect(url_for('root'))

    return render_template('edit_profile.html', form=form)
  
@app.route('/profile/<int:profile_id>')
def profile(profile_id):

    user = User.query.filter_by(id=profile_id).first_or_404()
    articles = Article.query.filter_by(user_id=profile_id).order_by(Article.date_created.desc())
    return render_template('profile.html', profile_user=user, articles=articles)
  
