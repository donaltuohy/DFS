from flask import Flask, render_template, url_for, request, session, redirect
#from flask.ext.pymongo import PyMongo

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Hi there how you doing"


if __name__ == "__main__":
    app.run()