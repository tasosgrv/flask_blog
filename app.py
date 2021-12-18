from flask import Flask

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def root():
    return  "<h3>hello flask</h3>"
    
@app.route('/hello')
def hello():
    return "hello"

@app.route('/hello/<name>')
def helloName(name):
    return f"hello {name}"

@app.route('/id/<int:name>')
def id(name):
    return f"id {name}"

if __name__=="__main__":
    app.run(debug=True)