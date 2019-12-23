from decimal import *
import datetime


def get_reviews(soup, dictionary):
    reviews = soup.find_all("div", {"class": "single-review"})
    amount_reviews = len(reviews) if reviews else 0

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
                        "rating": float(round(Decimal(review_rating["aria-label"].split("stars")[0].replace("Rated", "").strip()), 3)) if review_rating else review_rating,
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
                        "app_name": dictionary["name"]
                        }

        data_reviews.append(current_review)

    return dictionary, data_reviews


def get_date(string_date):
    """Docstring
    """
    date_time_obj = datetime.datetime.strptime(string_date, "%B %d, %Y")

    return date_time_obj
