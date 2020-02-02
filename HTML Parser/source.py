from bs4 import BeautifulSoup
import os
import pymongo
import utils.app_info as ai
import utils.reviews_info as ri
import utils.extra_apps_info as eai
import sys

ignore_folders = ["2017115-20171111%br%editorChoice%cc.pacer.androidapp.html",
                  "appsRetrieved.json", "processed", "raw_html", "RESULTS", "testData", "toProcess",
                  "20171105-20171111", "20171112-20171118", "20171119-20171125","20171126-20171202","20171126-20171202",
                  "20171203-20171209","20171210-20171216","20171217-20171223","20171224-20171230","20171231-201816",
                  "20180107-20180113","20180114-20180120","20180121-20180127","20180128-20180203","20180204-20180210",
                  "20180211-20180217", "20180218-20180224",
                  #"20180225-20180303", "20180304-20180310","20180311-20180317","20180318-20180324","20180325-20180331",
                  #"20180401-20180407","20180408-20180414","20180415-20180421","20180422-20180428","20180429-20180505",
                  #"20180506-20180512","20180513-20180519","20180520-20180526","20180527-20180602"
                  ]

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mining"]

is_testing_mode = True


def main(path_o:str):
    folders = os.listdir(path_o)

    for current_folder in folders:
        if current_folder not in ignore_folders:
            path = f'{path_o}/{current_folder}'

            files_folder = os.listdir(path)
            files_folder.sort()
            files_amount = len(files_folder)
            print(f'AMOUNT OF FILES {files_amount}')

            for counter, file in enumerate(files_folder):
                print(str(counter + 1), "-", file)

                with open(os.path.join(path, file), "r", encoding="utf8") as html_file:
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


                dictionary, data_reviews = ri.get_reviews(soup, dictionary, is_new_page, file)

                dictionary, data_similar = eai.get_apps(soup, \
                                                        "cards expandable id-card-list", dictionary, "similar",
                                                        is_new_page)
                dictionary, data_more = eai.get_apps(soup, \
                                                     "more-from-developer", dictionary, "more_from_developer",
                                                     is_new_page)

                extra_apps = data_similar
                extra_apps.extend(data_more)

                save_mongo("app", [dictionary])
                save_mongo("reviews", data_reviews)
                save_mongo("extra_app", extra_apps)

                print(f'WRITTEN {counter + 1} apps more')

            print("")


def save_mongo(collection_db, data):
    print("-*-" * 5)
    if len(data) > 0:
        db[collection_db].insert_many(data)
    print("-*-" * 5)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Root folder's path is not given")
        sys.exit(1)
    else:
        main(sys.argv[1])
