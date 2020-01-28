from decimal import *
import datetime


def get_reviews(soup, dictionary, is_new_page, file):
    reviews = soup.find_all("div", {"class": "single-review"})
    amount_reviews = len(reviews) if reviews else 0

    if is_new_page and amount_reviews == 0:
        amount_reviews = None

    # "2017115-20171111%br%editorChoice%cc.pacer.androidapp.html"
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

    return dictionary, data_reviews


def get_date(string_date):
    date_time_obj = datetime.datetime.strptime(string_date, "%B %d, %Y")

    return date_time_obj


def get_retrieved_date(retrieved_date):

    return datetime.datetime.strptime(retrieved_date, "%Y%m%d")
