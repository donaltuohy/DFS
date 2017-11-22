from flask import Flask, render_template, url_for, request, session, redirect
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'dfs'
app.config['MONGO_URI'] = 'mongodb://donal:testing@ds117156.mlab.com:17156/dfs'

mongo = PyMongo(app)

@app.route('/add')
def add():
    files = mongo.db.files
    files.insert({'name': 'testingFilename'})
    return "Added name!"


if __name__ == "__main__":
    app.run(debug=True)