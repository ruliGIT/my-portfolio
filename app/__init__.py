import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


class Proj:
    def __init__(self, name, descrip, git, demo) -> None:
        self.name = name
        self.descrip = descrip
        self.git = git
        self.demo = demo


class Polaroid:
    def __init__(self, caption, pic):
        self.caption = caption
        self.pic = pic


class Exp:
    def __init__(self, name, descrip) -> None:
        self.name = name
        self.descrip = descrip


pols = [
    Polaroid("drawing", "./static/img/drawing.png"),
    Polaroid("cooking", "./static/img/cooking.png"),
    Polaroid("traveling",
             "./static/img/traveling.png")
]


@app.route('/')
def index():

    projs = [
        Proj("Proj 1", "Description of my proj 1!",
             "https://google.com/", "https://github.com/"),
        Proj("Proj 2", "This is my proj 2!!",
             "https://github.com/", "https://github.com/"),
        Proj("Proj 3", "Description of my proj 3",
             "https://github.com/", "https://github.com/"),
        Proj("Proj 4", "Description of my proj 4",
             "https://github.com/", "https://github.com/")
    ]

    exps = [
        Exp("Experience 1", ["point 1", "point 2", "point 3"]),
        Exp("Experience 2", ["point 1", "point 2", "point 3"]),
        Exp("Experience 3", ["point 1", "point 2", "point 3"]),
        Exp("Experience 4", ["point 1", "point 2", "point 3"])
    ]

    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), projects=projs, polaroids=pols, experiences=exps)


@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', url=os.getenv("URL"), polaroids=pols)
