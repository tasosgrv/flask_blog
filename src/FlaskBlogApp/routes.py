from flask import (current_app, render_template, 
                    redirect, 
                    url_for,
                    request, 
                    flash)
from FlaskBlogApp.forms import NewArticleForm, SignupForm, LoginForm, NewArticleForm, AccountUpdateForm
from FlaskBlogApp import app, db, bcrypt
from FlaskBlogApp.models import User, Article

from flask_login import login_user, logout_user, current_user, login_required


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
        
        article = Article(article_title=form.article_title.data, article_body=form.article_body.data, author=current_user)

        db.session.add(article)
        db.session.commit()
        flash(f"O χρήστης <b>{current_user.username}</b> προσθεσε ενα άρθρο με επιτυχία","success")
        return redirect(url_for('root'))

    return render_template('new_article.html', form=form)


@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):

    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()

    form = NewArticleForm(article_title=article.article_title, article_body=article.article_body)

    if request.method == 'POST' and form.validate_on_submit():
        article.article_title = form.article_title.data
        article.article_body = form.article_body.data
        db.session.commit()

        flash(f"Το άρθρο με τίτλο {article.article_title} επεξεργάστηκε  με επιτυχία", "success")
        return redirect(url_for('root'))

    return render_template('new_article.html', form=form)


@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():

    form = AccountUpdateForm(username=current_user.username, email=current_user.email)

    if request.method == 'POST' and form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash(f"Η ενημέρωση των στοιχείων του χρήστη <b>{current_user.username}</b> έγινε με επιτυχία","success")
        return redirect(url_for('root'))

    return render_template('account_update.html', form=form)
  
