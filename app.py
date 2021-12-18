from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return '''
    <htnl>
    <head><title>Τιτλος</title></head>
    <body>
    <h3>hello flask</h3>
    </body>
    </html>
    '''
    


if __name__=="__main__":
    app.run()