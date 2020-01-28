import os
from bs4 import BeautifulSoup
import pymongo
import utils.app_info as ai
import utils.reviews_info as ri
import utils.extra_apps_info as eai

ignore_folders = ["2017115-20171111%br%editorChoice%cc.pacer.androidapp.html",
                  "appsRetrieved.json", "processed", "raw_html", "RESULTS", "testData", "toProcess"]

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mining"]

is_testing_mode = True


def main():
    folders = os.listdir("/Volumes/Elements/data")

    for current_folder in folders:
        if current_folder not in ignore_folders:
            path = f'/Volumes/Elements/data/{current_folder}'

            files_folder = os.listdir(path)
            files_folder.sort()
            files_amount = len(files_folder)
            print(f'AMOUNT OF FILES {files_amount}')

            for counter, file in enumerate(files_folder):
                print(str(counter + 1), "-", file)

                with open(os.path.join(path, file), "r") as html_file:
                    html_content = html_file.read()

                dictionary = {}

                soup = BeautifulSoup(html_content, "html.parser")

                is_new_page = False
                page_format = soup.find("base", {"href": "https://play.google.com/"})
                if page_format is not None:
                    is_new_page = True

                dictionary = ai.get_basic_info(soup, file, dictionary, is_new_page)
                dictionary = ai.get_tech_info(soup, dictionary, is_new_page)
                dictionary = ai.get_rating(soup, dictionary, is_new_page)
                dictionary = ai.get_whats_new(soup, dictionary, is_new_page)
                dictionary = ai.get_dev_info(soup, dictionary, is_new_page)

                dictionary, data_reviews = ri.get_reviews(soup, dictionary, is_new_page)

                dictionary, data_similar = eai.get_apps(soup, \
                                                        "cards expandable id-card-list", dictionary, "similar",
                                                        is_new_page)
                dictionary, data_more = eai.get_apps(soup, \
                                                     "more-from-developer", dictionary, "more_from_developer",
                                                     is_new_page)

                extra_apps = data_similar
                extra_apps.extend(data_more)

                save_mongo("app", [dictionary])
                save_mongo("review", data_reviews)
                save_mongo("extra_app", extra_apps)

                print(f'WRITTEN {counter + 1} apps more')

            print("")


def save_mongo(collection_db, data):
    print("-*-" * 5)
    if len(data) > 0:
        db[collection_db].insert_many(data)
    print("-*-" * 5)


if __name__ == "__main__":
    main()
