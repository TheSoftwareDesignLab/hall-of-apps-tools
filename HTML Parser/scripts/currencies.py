import pymongo
from decimal import *

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mining"]
coll = db["extra_app"]

currencies = {
    "br": "R$",
    "us": "$",
    "de": "€",
    "co": "COP",
}


def get_decimal_price(price, country):

	if "Free" in price:
		return 0.0
	else:
		price = price.replace(currencies[country], "").strip()
		if country in ["co", "us", "br"]:
			price = price.replace(",", "")
		elif country == "de":
			price = price.replace(",", ".")

		return float(round(Decimal(price), 2))


counter = 0
query = {"price": {"$type": "string"}}
cursor = coll.find(query)

try:
    for doc in cursor:
    	id_mongo = doc["_id"]
    	price = doc["price"]
    	country = doc["country"]
    	currency = ""

    	if price and country:
    		price = get_decimal_price(price, country)
    	if country:
    		currency = currencies[country]

    	print(currency)
    	print(price)
    	print("-------------------------")
    	newvalues = { "$set": { "price": price, "currency": currency } }
    	coll.update_one({"_id": id_mongo}, newvalues)
    	counter = counter + 1
    	print(counter)


finally:
    client.close()

