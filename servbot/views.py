
from servbot import app
#from flask import render_template
import helpers
from flask.ext.pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import json



@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('landing.html');



@app.route('/restaurants/', methods=['GET', 'POST'])
def restaurantList():
	
#app.config['MONGO_URI'] = 'mongodb://admin:admin@ds053678.mongolab.com:53678/servbot'
#app.config['MONGO_DBNAME'] = 'restaurants'
#app.config['MONGO_USERNAME'] = 'admin'
#app.config['MONGO_PASSWORD'] = 'admin'

#mongo = PyMongo(app, config_prefix = 'MONGO');
	client = MongoClient('mongodb://admin:admin@ds053678.mongolab.com:53678/servbot')
	db = client.servbot

#db.restaurants.insert({"name" : '',
#"tables" : [{
#	"number" : '',
#	"orders" : []
#		}
#	]
#})
#	db.restaurants.update(
#		{ "name" : ""
#		},
#		{ "$push" : {"tables.0.orders" : "woohoo"}
#		}
#	)
	index = 0
	cursor = db.restaurants.find().sort("name", 1)
	nameList = []
	for v in cursor:
		print v['name']
		nameList.append(v['name'])

	for greg in nameList:
		print ("%s" % greg)

	return json.dumps(nameList)
