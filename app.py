from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
app = Flask(__name__)
# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///first_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "users"    # optional
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    age = db.Column(db.Integer)
    # notice the extra import statement above
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())


@app.route("/")
def root():
    userlist = User.query.all()
    return render_template('index.html', userlist=userlist)


@app.route('/addUser', methods=['POST'])
def addUser():
    newUser = User(first_name=request.form['fName'], last_name=request.form['lName'],
                   email=request.form['email'], age=request.form['age'])
    db.session.add(newUser)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
