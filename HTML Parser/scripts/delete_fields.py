import pymongo
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mining"]
coll = db["app"]

#para que solo lea las primeras semanas
query = { "retrieved_date_start": { "$lt": datetime.datetime(2018,02,25) } }

cursor = coll.find(query)

try:
    for doc in cursor:

        id_mongo = doc["_id"]
        num_installs = doc["num_installs"]
        category = doc["category"]
        top = doc["top"]

        new_category = ""

        if category and top:
            if "editorchoice" in top.lower():
                new_category = top
            else:
                new_category = category + "_" + top

        if num_installs:
            if "10,000+" in num_installs:
                num_installs = "10,000 - 50,000"
            elif "50,000+" in num_installs:
                num_installs = "50,000 - 100,000"
            elif "100,000+" in num_installs:
                num_installs = "100,000 - 500,000"
            elif "500+" in num_installs:
                num_installs = "500 - 1,000"
            elif "5,000+" in num_installs:
                num_installs = "5,000 - 10,000"
            elif "50+" in num_installs:
                num_installs = "50 - 100"
            elif "100+" in num_installs:
                num_installs = "100 - 500"
            elif "1,000+" in num_installs:
                num_installs = "1,000 - 5,000"
            elif "10,000,000+" in num_installs:
                num_installs = "10,000,000 - 50,000,000"
            elif "1,000,000+" in num_installs:
                num_installs = "1,000,000 - 5,000,000"
            elif "5,000,000+" in num_installs:
                num_installs = "5,000,000 - 10,000,000"
            elif "500,000+" in num_installs:
                num_installs = "500,000 - 1,000,000"
            elif "50,000,000+" in num_installs:
                num_installs = "50,000,000 - 100,000,000"
            elif "5+" in num_installs:
                num_installs = "5 - 10"
            elif "100,000,000+" in num_installs:
                num_installs = "100,000,000 - 500,000,000"
            elif "10+" in num_installs:
                num_installs = "10 - 50"
            elif "1+" in num_installs or "0+" in num_installs:
                num_installs = "1 - 5"
            elif "1,000,000,000+" in num_installs:
                num_installs = "1,000,000,000 - 5,000,000,000"
            elif "500,000,000+" in num_installs:
                num_installs = "500,000,000 - 1,000,000,000"

        fixed_values = { "$set": { "category": new_category, "num_installs": num_installs },
                       "$unset": {"required_version": "", "has_specific_version": "", "price_usd": "", "has_whats_new": ""}
                    }
        coll.update_one({"_id": id_mongo}, fixed_values)
        counter = counter + 1
        print(counter)
finally:
    client.close()


