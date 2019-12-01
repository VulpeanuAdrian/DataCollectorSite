from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
import smtplib
from sqlalchemy.sql import func

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://kyjgdhzmewfryb:47172a6e65895290c8283f032b0cfdc220a7db598daad97abb6f1d16447138a4@ec2-174-129-205-197.compute-1.amazonaws.com:5432/d676vjst4s1bu2?sslmode=require'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__='data'
    id=db.Column(db.Integer,primary_key=True)
    email_=db.Column(db.String(120),unique=True)
    email_=db.Column(db.String(120),unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_



def send_email(email,height,average_height,count):
    from_email='vulpeanuadrian1994@gmail.com'
    from_password=""         #!! need to update password!
    to_email=email

    subject="Height data"
    message="Hey there, your height is <strong>%s</strong>." \
            "<br>Average height of all is %s." \
            "Calculate out of <strong>%s of people</strong>.<br>Thanks"%(height,average_height,count)

    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        height=request.form["height_name"]
        if db.session.query(Data).filter(Data.email_==email).count()==0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height_).count()
            send_email(email,height,average_height,count)
            return render_template("success.html")

    return render_template('index.html',text="Email already exist's in our DB")

if __name__ == '__main__':
    app.debug = True
    app.run()
