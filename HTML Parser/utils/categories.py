import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mining"]
coll = db["app"]

query = {}

cursor = coll.find(query)
counter = 0
try:
    for doc in cursor:
        if doc["category"]:
            id_mongo = doc["_id"]
            new_category = doc["category"].replace("_topFree", "").replace("_topSelling", "")
            print(new_category)
            newvalues = { "$set": { "category": new_category } }
            coll.update_one({"_id": id_mongo}, newvalues)
            counter = counter + 1
            print(counter)
finally:
    client.close()
