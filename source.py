import os
import pandas as pd
from bs4 import BeautifulSoup
import pymongo
import utils.app_info as ai
import utils.reviews_info as ri
import utils.extra_apps_info as eai


current_folder = "20171105-20171111"

path = "data/"

path = f'D:/lauBello/data/'

#path_processed = f"D:/lauBello/data/{current_folder}" 

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mining"]
#app_collection = db["app"]
#review_collection = db["review"]
#extra_app_collection = db["extra_app"]


def main():
    """ Here you have to put the documentation for the function
    """

    counter = 0

    files_folder = os.listdir(path)
    files_folder.sort()
    files_amount = len(files_folder)
    print(f'AMOUNT OF FILES {files_amount}')
    data = []
    reviews = []
    extra_apps = []

    for counter, file in enumerate(files_folder):
        
        print(str(counter), "-", file)

        with open(os.path.join(path,file), "r") as html_file:
            html_content = html_file.read()

        dictionary = {}

        soup = BeautifulSoup(html_content, "html.parser")
        dictionary = ai.get_basic_info(soup, file, dictionary)
        dictionary = ai.get_tech_info(soup, dictionary)
        dictionary = ai.get_rating(soup, dictionary)
        dictionary = ai.get_whats_new(soup, dictionary)
        dictionary = ai.get_dev_info(soup, dictionary)

        dictionary, data_reviews = ri.get_reviews(soup, dictionary)
        reviews.extend(data_reviews)

        dictionary, data_similar = eai.get_apps(soup,\
            "cards expandable id-card-list", dictionary, "similar")
        dictionary, data_more = eai.get_apps(soup,\
            "more-from-developer", dictionary, "more_from_developer")

        data.append(dictionary)
        extra_apps.extend(data_similar)
        extra_apps.extend(data_more)

        if counter == 1:
            save_mongo("app",data)
            save_mongo("review",reviews)
            save_mongo("extra_app",extra_apps)

            break

        if counter % 100 == 0:
            print(f'WRITTEN {counter+1} apps more')
            data = []
            reviews = []
            extra_apps = []

    print(f'WRITTEN {counter} apps more')


def save_mongo(collection_db, data):
    """
    """
    print("-*-"*5)
    db[collection_db].insert_many(data)
    print("-*-"*5)


if __name__ == "__main__":
    """ Ypu have to do the Python's main in this way. Otherwise all 
    kinds of linters and type corections runs all your code
    """
    main()
