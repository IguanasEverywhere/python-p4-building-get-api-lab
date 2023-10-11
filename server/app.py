#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = []
    bakeries = Bakery.query.all()
    for bakery in bakeries:
        new_bakery = bakery.to_dict()
        all_bakeries.append(new_bakery)
    return make_response(all_bakeries, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id==id).first()
    bakery_dict = bakery.to_dict()
    return make_response(bakery_dict, 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = []
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price))
    for good in baked_goods:
        new_good = good.to_dict()
        baked_goods_by_price.append(new_good)
    return make_response(baked_goods_by_price, 200)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive_goods = BakedGood.query.order_by(desc(BakedGood.price)).limit(1)
    good_dict = expensive_goods[0].to_dict()
    return make_response(good_dict, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
