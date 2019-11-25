from decimal import *
import datetime


def get_basic_info(soup, file, dictionary):

    app_id = soup.find("div", {"class": "details-wrapper apps"})
    app_name = soup.find("div", {"class": "id-app-title"})
    app_description = soup.find("meta", {"name": "description"})
    app_url = soup.find("meta", {"property": "og:url"})
    genre = soup.find("a", {"class": "document-subtitle category"}).span
    price = soup.find("meta", {"itemprop": "price"})
    description = soup.find("div", {"class": "show-more-content text-body", "itemprop": "description"}).get_text()

    file_info = file.split("%")
    retrieved_date = file_info[0].split("-")
    retrieved_date_start = retrieved_date[0]
    retrieved_date_end = retrieved_date[1]
    country = file_info[1]
    category = file_info[2]

    dictionary["id"] = "N/A" if app_id is None else app_id["data-docid"].strip()
    dictionary["name"] = "N/A" if app_name is None else app_name.string.strip()
    dictionary["summary"] = "N/A" if app_description is None else app_description["content"].strip()
    dictionary["url"] = "N/A" if app_url is None else app_url["content"].strip()
    dictionary["category"] = "N/A" if category is None else category
    dictionary["country"] = "N/A" if country is None else country

    dictionary["retrieved_date_start"] = get_retrieved_date("1990011") if retrieved_date_start is None else get_retrieved_date(retrieved_date_start)
    dictionary["retrieved_date_end"] = get_retrieved_date("1990011") if retrieved_date_end is None else get_retrieved_date(retrieved_date_end)

    dictionary["genre"] = ["N/A"] if genre is None else genre.string.split("&")
    dictionary["price"] = "N/A" if price is None else price["content"].strip()
    dictionary["description"] = "N/A" if description is None else description.strip()

    return dictionary


def get_rating(soup, dictionary):
    rating = soup.find("meta", {"itemprop": "ratingValue"})
    temp_5 = soup.find("div", {"class": "rating-bar-container five"})
    rating_5 = "0" if temp_5 is None else temp_5.find("span", {"class": "bar-number"}).string

    temp_4 = soup.find("div", {"class": "rating-bar-container four"})
    rating_4 = "0" if temp_4 is None else temp_4.find("span", {"class": "bar-number"}).string

    temp_3 = soup.find("div", {"class": "rating-bar-container three"})
    rating_3 = "0" if temp_3 is None else temp_3.find("span", {"class": "bar-number"}).string

    temp_2 = soup.find("div", {"class": "rating-bar-container two"})
    rating_2 = "0" if temp_2 is None else temp_2.find("span", {"class": "bar-number"}).string

    temp_1 = soup.find("div", {"class": "rating-bar-container one"})
    rating_1 = "0" if temp_1 is None else temp_1.find("span", {"class": "bar-number"}).string

    dictionary["rating"] = -1 if rating is None else float(round(Decimal(rating["content"]), 3))
    dictionary["rating_5"] = -1 if rating_5 is None else int(rating_5.replace(",", ""))
    dictionary["rating_4"] = -1 if rating_4 is None else int(rating_4.replace(",", ""))
    dictionary["rating_3"] = -1 if rating_3 is None else int(rating_3.replace(",", ""))
    dictionary["rating_2"] = -1 if rating_2 is None else int(rating_2.replace(",", ""))
    dictionary["rating_1"] = -1 if rating_1 is None else int(rating_1.replace(",", ""))

    return dictionary


def get_tech_info(soup, dictionary):
    date_updated = soup.find("div", {"itemprop": "datePublished"})
    num_installs = soup.find("div", {"itemprop": "numDownloads"})
    current_version = soup.find("div", {"itemprop": "softwareVersion"})
    android_versions = soup.find("div", {"itemprop": "operatingSystems"})
    content_rating = soup.find("div", {"itemprop": "contentRating"})

    dictionary["last_update"] = get_date("January 1, 1990") if date_updated is None else get_date(date_updated.string.strip())
    dictionary["num_installs"] = "N/A" if num_installs is None else num_installs.string.strip()
    dictionary["current_version"] = "N/A" if current_version is None else current_version.string.strip()
    dictionary["android_version"] = "N/A" if android_versions is None else android_versions.string.strip()
    dictionary["content_rating"] = "N/A" if content_rating is None else content_rating.string.strip()

    return dictionary


def is_dev_email(tag):
    if tag.has_attr("class") and tag.has_attr("href") and tag["href"].find("mailto") > -1:
        return True
    return False


def get_dev_info(soup, dictionary):
    dev = soup.find("a", {"class": "document-subtitle primary"}).span
    dev_mail = soup.find(is_dev_email)
    dev_address = soup.find("div", {"class": "content physical-address"})

    dictionary["dev_name"] = "N/A" if dev is None else dev.string
    dictionary["dev_mail"] = "N/A" if dev_mail is None else dev_mail.string.replace("Email", "").strip()
    dictionary["dev_address"] = "N/A" if dev_address is None else str(dev_address)

    return dictionary


def get_whats_new(soup, dictionary):
    temp = soup.find("div", {"class": "details-section whatsnew"})
    list_news = []

    if temp is not None and temp.div is not None:
        whats_new = temp.div
        news = whats_new.find_all("div", {"class": "recent-change"})
        for change in news:
            list_news.append(change.string.strip())

    dictionary["whats_new"] = list_news

    return dictionary


def get_date(string_date):

    return datetime.datetime.strptime(string_date, "%B %d, %Y")


def get_retrieved_date(retrieved_date):

    return datetime.datetime.strptime(retrieved_date, "%Y%m%d")
