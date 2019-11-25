from decimal import *
import datetime


def get_reviews(soup, dictionary):
    reviews = soup.find_all("div", {"class": "single-review"})
    amount_reviews = 0 if reviews is None else len(reviews)

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

        if review_title is not None:
            review_title = review_title.strip()
            review_text = review_text.replace(review_title, "").strip()

        review_parent = review.parent
        dev_comment = review_parent.find("div", {"class": "developer-reply"})

        dev_name = "N/A"
        dev_date = "January 1, 1990"
        dev_reply = "N/A"
        if dev_comment is not None:
            dev_name = dev_comment.div.find("span", {"class": "author-name"}).string
            dev_date = dev_comment.div.find("span", {"class": "review-date"}).string
            dev_reply = dev_comment.get_text().replace(dev_name, "").replace(dev_date, "").strip()

        current_review = {"author": "N/A" if review_author is None else review_author.string,
                          "date": "N/A" if review_date is None else get_date(review_date.string),
                          "rating": -1.0 if review_rating is None else float(round(Decimal(review_rating["aria-label"].split("stars")[0].replace("Rated", "").strip()),3)),
                          "title": "N/A" if review_title is None else review_title,
                          "text": review_text,
                          "dev_name": dev_name,
                          "dev_reply": dev_reply,
                          "dev_reply_date": get_date(dev_date),
                          "app_id": dictionary["id"],
                          "app_retrieved_date": dictionary["retrieved_date"],
                          "app_name": dictionary["name"]
                          }

        data_reviews.append(current_review)

    return dictionary, data_reviews


def get_date(string_date):
    date_time_obj = datetime.datetime.strptime(string_date, "%B %d, %Y")

    return date_time_obj
