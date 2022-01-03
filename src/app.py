from flask import (Flask, 
                    render_template, 
                    redirect, 
                    url_for,
                    request)

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def root():
    return  render_template('index.html')


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pasword = request.form['pasword']
        pasword2 = request.form['pasword2']
        print(username, email, pasword, pasword2)
    return render_template('signup.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/logout/')
def logout():
    return redirect(url_for('root'))

@app.route('/new_article/')
def new_article():
    return render_template('new_article.html')
  


if __name__=="__main__":
    app.run(debug=True)