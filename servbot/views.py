
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


@app.route('/order/', methods=['get', 'post'])
def addorders():
 
	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot
	price = db.tables.find({"number" : 2, "owner" : "TGI Fridays"})[0]["price"]
	print price
	price += db.menus.find({"owner" : "TGI Fridays", "number" : 3})[0]["price"]
	print price
	db.tables.update(
		{"number" : 2, "owner" : "TGI Fridays"},
		{ "$push" : {"orders" : "woohoo"},
		}
	)

	db.tables.update(
		{"number" : 2, "owner" : "TGI Fridays"},
		{ "$set" : {"price" : price},
		}
	)
	return peekOrder()	


@app.route('/peekOrder/', methods=['get', 'post'])
def peekOrder():
 
	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot
 	return json.dumps(db.tables.find_one({'owner' : "TGI Fridays", 'number': 2})["orders"])



@app.route('/insertToMenu/', methods=['get', 'post'])
def addMenus():
 
	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot

	db.menus.insert({"owner" : 'TGI Fridays',
		"number" : 3,
		"description" : "ribs",
		"price" : 13.99
})
	return json.dumps(db.menus.find_one({"owner" : 'TGI Fridays', "number" : 3})["description"])


@app.route('/menus/', methods=['get', 'post'])
def getMenus():
 	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot

	menu = []
	cursor2 = db.menus.find({"owner" : 'TGI Fridays'}).sort("number" , 1)
	for c in cursor2:
		menu.append(c["description"])
 	return json.dumps(menu)

@app.route('/getPrice/', methods=['get', 'post'])
def getPrice():
 	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot

	cursor4 = db.menus.find_one({"owner" : 'TGI Fridays'})
 	return json.dumps(cursor4["price"])



@app.route('/checkoutPrice/', methods=['get', 'post'])
def checkoutPrice():
 	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot
 	return json.dumps(db.tables.find_one({"number" : 2, "owner" : "TGI Fridays"})["price"])


