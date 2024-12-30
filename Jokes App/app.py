from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from pyjokes import get_joke
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#TODO: Create the database model
class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    joke = db.Column(db.Text)
    created_at = db.Column(db.DateTime())
    
    def __init__(self, joke):
        self.joke = joke
        self.created_at = datetime.now()

@app.route("/")
def index():
    jokes = Joke.query.order_by(desc(Joke.created_at)).all()
    return render_template('index.html', jokes=jokes)

@app.route('/show_joke', methods=['GET', 'POST'])
def show_joke():
    if request.method == 'POST':
        joke = get_joke(language="en", category="all")
        newJoke = Joke(joke=joke)
        db.session.add(newJoke)
        db.session.commit()
        return redirect('/')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)