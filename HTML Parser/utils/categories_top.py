import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mining"]
coll = db["app"]

query = {}

cursor = coll.find(query)
counter = 0
try:
    for doc in cursor:
        if doc["category"] and doc["top"]:
            id_mongo = doc["_id"]
            category = doc["category"]
            top = doc["top"]

            if "editorchoice" in top.lower():
                new_category = top
            else:
                new_category = category + "_" + top

            print(new_category)
            newvalues = { "$set": { "category_top": new_category } }
            coll.update_one({"_id": id_mongo}, newvalues)
            counter = counter + 1
            print(counter)
finally:
    client.close()
