import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import requests
import urllib
import hashlib
import sys
from requests.models import Response
import re

load_dotenv()
app = Flask(__name__)

dataf = open("app/static/data.json",  encoding="utf-8")
data = json.load(dataf)


@app.route('/')
def index():

    projs = data['projs']
    exps2 = data['experiences']
    hobbies = data['polaroids']

    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), projects=projs, polaroids=hobbies, experiences=exps2)


@app.route('/hobbies')
def hobbies():
    hobbies = data['polaroids']
    return render_template('hobbies.html', url=os.getenv("URL"), polaroids=hobbies)


# MySQL Database

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                         user=os.getenv("MYSQL_USER"),
                         password=os.getenv("MYSQL_PASSWORD"),
                         host=os.getenv("MYSQL_HOST"),
                         port=3306)

print(mydb)

# TimelinePost peewee model


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

# TimelinePost api routes


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
         
    timeline_post = TimelinePost.create(
        name=name, email=email, content=content)
    return model_to_dict(timeline_post)
        
        
        

        


@app.route('/api/timeline_post/<int:id>', methods=['DELETE'])
def delete_time_line_post_byid(id):
    TimelinePost.get_by_id(id).delete_instance()
    return "Successfully deleted"


@app.route('/api/timeline_post/<string:name>', methods=['DELETE'])
def delete_time_line_post_byname(name):
    post = TimelinePost.get(TimelinePost.name == name)
    post.delete_instance()
    return "Successfully deleted\n"


@app.route('/timeline')
def timeline():
    posts = get_time_line_post()
    pfps = []
    email = "someone@somewhere.com"
    default = "https://cdn-icons-png.flaticon.com/512/149/149071.png"
    size = 40

    for i in posts["timeline_posts"]:
        email = i["email"].encode('utf-8')
        gravatar_url = "https://www.gravatar.com/avatar/" + \
            hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.parse.urlencode({'d': default, 's': str(size)})
        pfps.append(gravatar_url)

    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"), num=len(posts["timeline_posts"]), posts=posts["timeline_posts"], pfps=pfps)
