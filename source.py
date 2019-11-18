import os
import pandas as pd
from bs4 import BeautifulSoup
import utils.app_info as ai
import utils.reviews_info as ri
import utils.extra_apps_info as eai


current_folder = "20171105-20171111"
path = "/home/mariacamila/Documents/Laura/data/%s/" % current_folder
path_processed = "/home/mariacamila/Documents/Laura/processed/%s/" % current_folder


def main():

    counter = 0

    files_folder = os.listdir(path)
    files_folder.sort()
    files_amount = len(files_folder)
    print("AMOUNT OF FILES {0}".format(files_amount))
    data = []
    reviews = []
    extra_apps = []

    for file in files_folder:
        counter += 1
        print(str(counter) + "-" + file)
        html_file = open(path + file, "r")
        html_content = html_file.read()
        html_file.close()

        dictionary = {}

        soup = BeautifulSoup(html_content, "html.parser")
        dictionary = ai.get_basic_info(soup, file, dictionary)
        dictionary = ai.get_tech_info(soup, dictionary)
        dictionary = ai.get_rating(soup, dictionary)
        dictionary = ai.get_dev_info(soup, dictionary)

        dictionary, data_reviews = ri.get_reviews(soup, dictionary)
        reviews.extend(data_reviews)

        dictionary, data_similar = eai.get_apps(soup, "cards expandable id-card-list", dictionary, "similar")
        dictionary, data_more = eai.get_apps(soup, "more-from-developer", dictionary, "more-from-developer")

        data.append(dictionary)
        extra_apps.extend(data_similar)
        extra_apps.extend(data_more)

        if counter % 100 == 0:
            write_csv(data, reviews, extra_apps, counter)
            print("WRITTEN {0} apps more".format(counter))
            data = []
            reviews = []
            extra_apps = []

    write_csv(data, reviews, extra_apps, counter)
    print("WRITTEN {0} apps more".format(counter))


def read_csv(csv_path):
    current_csv = pd.read_csv(csv_path)
    print(csv_path + " " + str(current_csv.shape))


def write_csv(data, reviews, extra_apps, counter):
    df_apps = pd.DataFrame(data)
    df_reviews = pd.DataFrame(reviews)
    df_extra_apps = pd.DataFrame(extra_apps)

    if not os.path.exists(path_processed):
        os.mkdir(path_processed)

    apps_path = "{0}apps{1}.csv".format(path_processed, counter)
    reviews_path = "{0}reviews{1}.csv".format(path_processed, counter)
    extra_apps_path = "{0}extra_apps{1}.csv".format(path_processed, counter)

    df_apps.to_csv(apps_path, index=False)
    df_reviews.to_csv(reviews_path, index=False)
    df_extra_apps.to_csv(extra_apps_path, index=False)


main()