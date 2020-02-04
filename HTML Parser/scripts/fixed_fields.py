import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mining"]
coll = db["app"]

query = {}

cursor = coll.find(query)
counter = 0
try:
    for doc in cursor:
        id_mongo = doc["_id"]
        num_installs = doc["num_installs"]
        android_version = doc["android_version"]
        required_version = ""
        has_specific_version = False
        price = doc["price"]
        price_usd = 0.0
        whats_new = doc["whats_new"]
        has_whats_new = False
        country = doc["country"]

        if num_installs:
            if "10,000 - 50,000" in num_installs:
                num_installs = "10,000+"
            elif "50,000 - 100,000" in num_installs:
                num_installs = "50,000+"
            elif "100,000 - 500,000" in num_installs:
                num_installs = "100,000+"
            elif "500 - 1,000" in num_installs:
                num_installs = "500+"
            elif "5,000 - 10,000" in num_installs:
                num_installs = "5,000+"
            elif "50 - 100" in num_installs:
                num_installs = "50+"
            elif "100 - 500" in num_installs:
                num_installs = "100+"
            elif "1,000 - 5,000" in num_installs:
                num_installs = "1,000+"
            elif "10,000,000 - 50,000,000" in num_installs:
                num_installs = "10,000,000+"
            elif "1,000,000 - 5,000,000" in num_installs:
                num_installs = "1,000,000+"
            elif "5,000,000 - 10,000,000" in num_installs:
                num_installs = "5,000,000+"
            elif "500,000 - 1,000,000" in num_installs:
                num_installs = "500,000+"
            elif "50,000,000 - 100,000,000" in num_installs:
                num_installs = "50,000,000+"
            elif "5 - 10" in num_installs:
                num_installs = "5+"
            elif "100,000,000 - 500,000,000" in num_installs:
                num_installs = "100,000,000+"
            elif "10 - 50" in num_installs:
                num_installs = "10+"
            elif "1 - 5" in num_installs or "0+" in num_installs:
                num_installs = "1+"
            elif "1,000,000,000 - 5,000,000,000" in num_installs:
                num_installs = "1,000,000,000+"
            elif "500,000,000 - 1,000,000,000" in num_installs:
                num_installs = "500,000,000+"

        if android_version:
            android_version = android_version.strip()
            if android_version in ["1.1 and up", "1.0 and up", "1.0 - 6.0"]:
                required_version = "Unnamed and up"
            elif android_version in ["1.5 and up"]:
                required_version = "Cupcake and up"
            elif android_version in ["1.6 and up"]:
                required_version = "Donut and up"
            elif android_version in ["2.1 and up", "2.1 - 6.0", "2.0.1 and up", "2.0 and up", "2.0 - 4.3"]:
                required_version = "Eclair and up"
            elif android_version in ["2.2 and up"]:
                required_version = "Froyo and up"
            elif android_version in ["2.3.3 and up", "2.3.3 - 6.0", "2.3 and up", "2.3 - 8.0", "2.3 - 7.0"]:
                required_version = "Gingerbread and up"
            elif android_version in ["3.2 and up", "3.1 and up", "3.0 and up", "3.0 - 8.0", "3.0 - 7.1.1"]:
                required_version = "Honeycomb and up"
            elif android_version in ["4.0.3 and up", "4.0.3 - 7.1.1", "4.0.3 - 6.0", "4.0 and up", "4.0 - 8.0", "4.0 - 7.1.1"]:
                required_version = "Ice Cream Sandwich and up"
            elif android_version in ["4.3 and up", "4.3 - 8.0", "4.3 - 7.1.1", "4.2 and up", "4.2 - 8.0", "4.2 - 7.1.1", "4.1 and up", "4.1 - 8.0", "4.1 - 7.1.1"]:
                required_version = "Jelly Bean and up"
            elif android_version in ["4.4W and up", "4.4 and up", "4.4 - 8.0", "4.4 - 7.1.1", "4.4"]:
                required_version = "KitKat and up"
            elif android_version in ["5.1 and up", "5.1 - 7.1.1", "5.0 and up", "5.0 - 8.0", "5.0 - 7.1.1", "5.0 - 6.0"]:
                required_version = "Lollipop and up"
            elif android_version in ["6.0 and up"]:
                required_version = "Marshmallow and up"
            elif android_version in ["7.1 and up", "7.0 and up", "7.0"]:
                required_version = "Nougat and up"
            elif android_version in ["8.0 and up"]:
                required_version = "Oreo and up"
            elif android_version in ["Varies with device"]:
                required_version = "Varies with device"

            if "and up" in android_version:
                has_specific_version = False
            else:
                has_specific_version = True

        if price:
            if country == "co":
                price_usd = price/2881.97
            elif country == "br":
                price_usd = price/3.35
            elif country == "de":
                price_usd = price/0.83
            else:
                price_usd = price

        if whats_new:
            if len(whats_new) > 0:
                has_whats_new = True
            else:
                has_whats_new = False

        print("---------------")
        newvalues = { "$set": { "num_installs": num_installs, "required_version": required_version, "has_specific_version": has_specific_version, "price_usd": price_usd, "has_whats_new": has_whats_new}}
        coll.update_one({"_id": id_mongo}, newvalues)
        counter = counter + 1
        print(counter)
finally:
    client.close()
