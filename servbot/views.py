
from servbot import app
from flask import render_template
import helpers
import pymongo
from pymongo import MongoClient
import json



@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('landing2.html');



@app.route('/restaurants/', methods=['GET', 'POST'])
def restaurantList():
	
	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot

	index = 0
	cursor = db.restaurants.find()
	nameList = []
	for v in cursor:
		nameList.append(v['name'])

	return json.dumps(nameList);

@app.route('/restaurants/<restaurant>/<number>', methods=['get', 'post'])
def createTable(restaurant, number):
 
	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot

	db.tables.insert({"owner" : restaurant,
		"number" : number,
		"orders" : []
})
	return json.dumps(db.tables.find_one({"owner" : restaurant, "number" : number})["number"])


@app.route('/order/<restaurant>/<table>/<order>', methods=['get', 'post'])
def addorders(restaurant, table, order):
 
	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot
	price = db.tables.find_one({"number" : table, "owner" : restaurant})[0]["price"]
	price += db.menus.find({"owner" : restaurant, "number" : order})[0]["price"]
	db.tables.update(
		{"number" : table, "owner" : restaurant},
		{ "$push" : {"orders" : order }
		}
	)

	db.tables.update(
		{"number" : table, "owner" : restaurant},
		{ "$set" : {"price" : price},
		}
	)
	return peekOrder()	


@app.route('/peekOrder/<restaurant>/<order>', methods=['get', 'post'])
def peekOrder(restaurant, order):
 
	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot
 	return json.dumps(db.tables.find_one({'owner' : restaurant, 'number': order})["orders"])



@app.route('/insertToMenu/<restaurant>/<order>/<description>/<price>', methods=['get', 'post'])
def addMenus(restaurant, order, description,price):
 
	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot

	db.menus.insert({"owner" : restaurant,
		"number" : order,
		"description" : description,
		"price" : price
})
	return json.dumps(db.menus.find_one({"owner" : restaurant, "number" : order})["description"])


@app.route('/menus/<restaurant>', methods=['get', 'post'])
def getMenus(restaurant):
 	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot

	menu = []
	cursor2 = db.menus.find({"owner" : restaurant}).sort("number", 1) 
	for c in cursor2:
		menu.append(json.dumps({"name" : c["description"], "price" : c["price"]}))
 	return json.dumps(menu)

@app.route('/getPrice/<restaurant>', methods=['get', 'post'])
def getPrice(restaurant):
 	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot

	cursor4 = db.menus.find_one({"owner" : restaurant})
 	return json.dumps(cursor4["price"])



@app.route('/checkoutPrice/<restaurant>/<table>', methods=['get', 'post'])
def checkoutPrice(restaurant, table):
 	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot
 	return json.dumps(db.tables.find_one({"number" : "200", "owner" : "Applebees"})["price"])


