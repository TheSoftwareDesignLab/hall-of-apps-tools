import os
from bs4 import BeautifulSoup
import pymongo
import utils.app_info as ai
import utils.reviews_info as ri
import utils.extra_apps_info as eai


ignore_folders = ["20171105-20171111",
                  "20171112-20171118",
                  "20171119-20171125",
                  "20171126-20171202",
                  "20171203-20171209",
                  "20171210-20171216",
                  "20171217-20171223",
                  "20171224-20171230",
                  "20171231-201816",
                  "20180107-20180113",
                  "20180114-20180120",
                  "20180121-20180127",
                  "20180128-20180203",
                  "20180204-20180210",
                  "20180211-20180217",
                  "20180218-20180224",
                  "2017115-20171111%br%editorChoice%cc.pacer.androidapp.html",
                  "appsRetrieved.json", "processed", "raw_html", "RESULTS", "testData", "toProcess"]

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mining"]


def main():
    """ Here you have to put the documentation for the function
    """
    folders = os.listdir("/Volumes/Elements/data")

    for current_folder in folders:
        if current_folder not in ignore_folders:
            path = f'/Volumes/Elements/data/{current_folder}'
            files_folder = os.listdir(path)
            files_folder.sort()
            files_amount = len(files_folder)
            print(f'AMOUNT OF FILES {files_amount}')

            for counter, file in enumerate(files_folder):
        
                print(str(counter+1), "-", file)

                if current_folder == "20171217-20171223":
                    if counter < 14593:
                        continue

                with open(os.path.join(path, file), "r") as html_file:
                    html_content = html_file.read()

                dictionary = {}

                soup = BeautifulSoup(html_content, "html.parser")
                dictionary = ai.get_basic_info(soup, file, dictionary)
                dictionary = ai.get_tech_info(soup, dictionary)
                dictionary = ai.get_rating(soup, dictionary)
                dictionary = ai.get_whats_new(soup, dictionary)
                dictionary = ai.get_dev_info(soup, dictionary)

                dictionary, data_reviews = ri.get_reviews(soup, dictionary)

                dictionary, data_similar = eai.get_apps(soup,\
                    "cards expandable id-card-list", dictionary, "similar")
                dictionary, data_more = eai.get_apps(soup,\
                    "more-from-developer", dictionary, "more_from_developer")

                extra_apps = data_similar
                extra_apps.extend(data_more)

                save_mongo("app", [dictionary])
                save_mongo("review", data_reviews)
                save_mongo("extra_app", extra_apps)

                print(f'WRITTEN {counter + 1} apps more')

            print("")


def save_mongo(collection_db, data):
    """
    """
    print("-*-"*5)
    if len(data) > 0:
        db[collection_db].insert_many(data)
    print("-*-"*5)


if __name__ == "__main__":
    """ Ypu have to do the Python's main in this way. Otherwise all 
    kinds of linters and type corections runs all your code
    """
    main()
