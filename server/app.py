#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False # this is a configuration that has Json responses print on separate lines with indentation

migrate = Migrate(app, db)

db.init_app(app)

# / route
@app.route('/')
def index():
    return "Index for Game/Review/User API"

# /games route

@app.route('/games/')
def games():

    # setup empty array

    games = []

    # get_first_ten =  Game.query.limit(10).all()
    # sort_by_title = Game.query.order_by(Game.title).all()

    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)
    response = make_response(
        jsonify(games), # jsonify is a method in flask that serializes arguments as json and returns a reponse object
        200
        #{"Content-Type": "application/json"} use this if you dont want to use jsonify since its unecessary
    )

    return response

# games route with id

@app.route('/games/<id>')
def find_game_by_id(id):

    game = Game.query.filter(Game.id==id).first()

    if not game:
        return "404 not found"

    """ game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
    } """ # if we use serialize in our models we dont have to build this dictionary every time

    game_dict = game.to_dict()

    response = make_response(
        jsonify(game_dict), 
        200
    )

    response.headers["Content-Type"] = "application/json"

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)