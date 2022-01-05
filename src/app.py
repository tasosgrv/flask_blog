from flask import (Flask, 
                    render_template, 
                    redirect, 
                    url_for,
                    request)
from forms import SignupForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'TASOS'

@app.route('/index')
@app.route('/')
def root():
    return  render_template('index.html')


@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        print(username, email, password, password2)
    return render_template('signup.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

    return render_template('login.html', form=form)

@app.route('/logout/')
def logout():
    return redirect(url_for('root'))

@app.route('/new_article/')
def new_article():
    return render_template('new_article.html')
  


if __name__=="__main__":
    app.run(debug=True)