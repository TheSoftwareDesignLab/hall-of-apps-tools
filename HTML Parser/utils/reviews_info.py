import datetime
from decimal import *
import json
import re
import pdb


def get_date(string_date):

    date_time_obj = datetime.datetime.strptime(string_date, "%B %d, %Y")
    return date_time_obj


def get_retrieved_date(retrieved_date):

    return datetime.datetime.strptime(retrieved_date, "%Y%m%d")


def script_in_text(id_tag=False,key='ds:13'):

    def regex_f(tag):

        return tag.name == 'script' and key in tag.get_text() and 'return' in tag.get_text() 

    def regex_id(tag):

        return tag.name == 'script' and '1.36880256E8' in tag.get_text() 

    function = regex_id if id_tag else regex_f
    
    return function

def get_field(field, review):

    try:
        if field=='author':
            response=review[1][0] 

        elif field=='rating':
            response=review[2] 

        elif field=='date':
            response=review[5][0] 

        elif field=='review_text':
            response=review[4] 

        elif field=='dev_name':
            response=review[7][0] 

        elif field=='dev_reply':
            response=review[7][1] 

        elif field=='dateReply':
            response=review[7][2][0] 
    except Exception as e:
        print(field,)
        response = None
    return response

def get_key_reviews(soup):

    script = soup.find_all(script_in_text(True))
    txt_id_reviews = script[0].get_text()
    key = None

    try:
        line_key = re.search('.*1.36880256E8.*\n', txt_id_reviews).group(0)

        if 'ds:13' in line_key:
            key=  'ds:13'
        elif 'ds:14' in line_key:
            key = 'ds:14'

    except Exception  as e:
        print(e)
        pass

    return key


def get_new_reviews(soup, dictionary):

    key = get_key_reviews(soup)

    data_reviews = []


    if key is not None:

        # info reviews
        script = soup.find_all(script_in_text(False,key)) #-------------------------------------------------missing key
        text_script = script[0].get_text() # text for script tag
        info_reviews = text_script[text_script.find("return")+7:text_script.find("}});")] # finds return and locates array reviews
        info_reviews = json.loads(info_reviews)


        try:
            for review in info_reviews[0]:

                current_review = {
                    "rating": get_field('rating',review),
                    "author": get_field('author',review),
                    "text": get_field('review_text',review),
                    "date": get_field('date',review),
                    #developer name that answers
                    "dev_name": get_field('dev_name',review),
                    "dev_reply": get_field('dev_reply',review),
                    "dev_reply_date": get_field('dateReply',review),
                    #data from app
                    "app_id": dictionary["id"],
                    "app_retrieved_date_start": dictionary["retrieved_date_start"],
                    "app_retrieved_date_end": dictionary["retrieved_date_end"],
                    "app_name": dictionary["name"],
                    "category": dictionary["category"],
                    "country": dictionary["country"]
                }

                data_reviews.append(current_review)
        
        except Exception  as e:
            print("no reviews")
            pass

    return data_reviews



def get_reviews(soup, dictionary, is_new_page, file):

    reviews = soup.find_all("div", {"class": "single-review"})
    amount_reviews = len(reviews) if reviews else 0

    if is_new_page and amount_reviews == 0:
        amount_reviews = 0
    
    # basic information from the file name
    file_info = file.split("%")
    retrieved_date = file_info[0].split("-")
    retrieved_date_start_file = retrieved_date[0]
    retrieved_date_end_file = retrieved_date[1]
    country = file_info[1]
    category = file_info[2]
    file_id = file_info[3].replace(".html", "")

    retrieved_date_start = get_retrieved_date(retrieved_date_start_file) if retrieved_date_start_file else retrieved_date_start_file
    retrieved_date_end = get_retrieved_date(retrieved_date_end_file) if retrieved_date_end_file else retrieved_date_end_file

    dictionary["id"] = file_id
    dictionary["retrieved_date_start"] = retrieved_date_start
    dictionary["retrieved_date_end"] = retrieved_date_end
    dictionary["category"] = category
    dictionary["country"] = country

    dictionary["amount_reviews"] = amount_reviews
    data_reviews = []

    # data from reviews
    for review in reviews:

        review_info = review.find("div", {"class": "review-header"}).find("div", {"class": "review-info"})
        review_content = review.find("div", {"class": "review-body with-review-wrapper"})
        review_author = review_info.find("span", {"class": "author-name"})
        review_date = review_info.find("span", {"class": "review-date"})

        review_rating = review_info.find("div", {"class": "tiny-star star-rating-non-editable-container"})
        review_title = review_content.find("span", {"class": "review-title"}).string
        review_text = review_content.get_text().replace("Full Review", "")

        if review_title:
            review_title = review_title.strip()
            review_text = review_text.replace(review_title, "").strip()

        review_parent = review.parent
        dev_comment = review_parent.find("div", {"class": "developer-reply"})

        dev_name = None
        dev_date = None
        dev_reply = None

        if dev_comment:
            dev_name = dev_comment.div.find("span", {"class": "author-name"}).string
            dev_date = dev_comment.div.find("span", {"class": "review-date"}).string
            dev_reply = dev_comment.get_text().replace(dev_name, "").replace(dev_date, "").strip()

        author = review_author.string if review_author else review_author
        date = get_date(review_date.string) if review_date else review_date
        app_id = dictionary["id"]

        current_review = {
            "rating": float(round(Decimal(review_rating["aria-label"].split("stars")[0].replace("Rated", "").strip()),
                                  3)) if review_rating else review_rating,
            "title": review_title,
            "author": author,
            "text": review_text,
            "date": date,
            "dev_name": dev_name,
            "dev_reply": dev_reply,
            "dev_reply_date": get_date(dev_date) if dev_date else dev_date,
            "app_id": app_id,
            "app_retrieved_date_start": dictionary["retrieved_date_start"],
            "app_retrieved_date_end": dictionary["retrieved_date_end"],
            "app_name": dictionary["name"],
            "category": dictionary["category"],
            "country": dictionary["country"]
        }

        data_reviews.append(current_review)

    if is_new_page:
        new_reviews = get_new_reviews(soup, dictionary)
        dictionary["amount_reviews"] = dictionary["amount_reviews"]  + len(new_reviews)
        data_reviews.extend(new_reviews)

    return dictionary, data_reviews