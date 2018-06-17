from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sendmail import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://rnmumskididfrc:4219e9075bdff1a4d75e5a44c6e61c0efbf17528a1f7ac800727c0d9e05faf44@ec2-23-23-247-245.compute-1.amazonaws.com:5432/d6827kvv6f4g57?sslmode=require'
db = SQLAlchemy(app)

class Data(db.Model):

    __tablename__ = "data"
    id=db.Column(db.Integer, primary_key = True)
    email_= db.Column(db.String(120), unique=True)
    height_= db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_=email_
        self.height_ = height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height_name"]

        if db.session.query(Data).filter(Data.email_==email).count()==0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height,1)
            count = db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            return render_template("success.html")

        return render_template("index.html",
               text="Seems like email address already present!")

if __name__ == '__main__':
    app.debug=True
    app.run()
