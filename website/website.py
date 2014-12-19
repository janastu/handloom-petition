from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import jsonify
from pymongo import MongoClient
import config as conf
from json import dumps


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/sign", methods=['POST'])
def signPetition():
    dbClient = MongoClient()
    db = dbClient[conf.DB]
    siteContent = db['content']
    """Check if the email already exists in the database. If an email exists
    then do not add it again, send error to client and tell email already
    exists.
    """
    test = siteContent.find_one({"email": request.form['email']})
    if test is None:
        siteContent.insert({"name": request.form['name'],
                            "email": request.form['email']})
        response = {"status": "Success",
                    "code": 1}
    else:
        response = {"status": "Duplicate email",
                    "code": 0}
    dbClient.disconnect()
    return jsonify(response)


@app.route("/users", methods=["GET"])
def getUsers():
    dbClient = MongoClient()
    db = dbClient[conf.DB]
    siteContent = db['content']
    skip = conf.NUMBER_OF_ITEMS * (int(request.args['page']) - 1)
    result = []
    for content in siteContent.find().skip(skip).limit(conf.NUMBER_OF_ITEMS):
        del(content['_id'])
        result.append(content)
    response = make_response()
    response.data = dumps(result)
    dbClient.disconnect()
    return response


@app.route("/count", methods=['GET'])
def getUserCount():
    dbClient = MongoClient()
    db = dbClient[conf.DB]
    siteContent = db['content']
    count = siteContent.count()
    dbClient.disconnect()
    return jsonify({"count": count})

if __name__ == "__main__":
    app.run(host=conf.HOST, port=conf.PORT, debug=True)