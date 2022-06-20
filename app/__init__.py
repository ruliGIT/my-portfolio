import os
from xmlrpc.client import DateTime
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict



load_dotenv()
app = Flask(__name__)
dataf = open("app/static/data.json",  encoding="utf-8")
data = json.load(dataf)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), user=os.getenv("MYSQL_USER"),
                     password=os.getenv("MYSQL_PASSWORD"), host=os.getenv("MYSQL_HOST"), port=3306)
print(mydb)

# peewee model
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

#timelinepost api
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/')
def index():

    projs = data['projs']
    exps2 = data['experiences']
    hobbies = data['polaroids']

    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), projects=projs, polaroids=hobbies, experiences=exps2)


@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', url=os.getenv("URL"), polaroids=hobbies)

