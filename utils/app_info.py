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

    dictionary["name"] = app_name.string.strip() if app_name else app_name
    dictionary["summary"] = app_description["content"].strip() if app_description else app_description
    dictionary["url"] = app_url["content"].strip() if app_url else app_url
    dictionary["category"] = category
    dictionary["country"] = country

    id_id = app_id["data-docid"].strip() if app_id else app_id
    retrieved_date_start = get_retrieved_date(retrieved_date_start) if retrieved_date_start else retrieved_date_start
    retrieved_date_end = get_retrieved_date(retrieved_date_end) if retrieved_date_end else retrieved_date_end

    dictionary["_id"] = {}
    dictionary["_id"]["id"] = id_id
    dictionary["_id"]["retrieved_date_start"] = retrieved_date_start
    dictionary["_id"]["retrieved_date_end"] = retrieved_date_end

    dictionary["genre"] = genre.string.split("&") if genre else genre
    dictionary["price"] = price["content"].strip() if price else price
    dictionary["description"] = description.strip() if description else description

    return dictionary


def get_rating(soup, dictionary):
    rating = soup.find("meta", {"itemprop": "ratingValue"})
    temp_5 = soup.find("div", {"class": "rating-bar-container five"})
    rating_5 = temp_5.find("span", {"class": "bar-number"}).string if temp_5 else temp_5

    temp_4 = soup.find("div", {"class": "rating-bar-container four"})
    rating_4 = temp_4.find("span", {"class": "bar-number"}).string if temp_4 else temp_4

    temp_3 = soup.find("div", {"class": "rating-bar-container three"})
    rating_3 = temp_3.find("span", {"class": "bar-number"}).string if temp_3 else temp_3

    temp_2 = soup.find("div", {"class": "rating-bar-container two"})
    rating_2 = temp_2.find("span", {"class": "bar-number"}).string if temp_2 else temp_2

    temp_1 = soup.find("div", {"class": "rating-bar-container one"})
    rating_1 = temp_1.find("span", {"class": "bar-number"}).string if temp_1 else temp_1

    dictionary["rating"] = float(round(Decimal(rating["content"]), 3)) if rating else rating
    dictionary["rating_5"] = int(rating_5.replace(",", "")) if rating_5 else rating_5
    dictionary["rating_4"] = int(rating_4.replace(",", "")) if rating_4 else rating_4
    dictionary["rating_3"] = int(rating_3.replace(",", "")) if rating_3 else rating_3
    dictionary["rating_2"] = int(rating_2.replace(",", "")) if rating_2 else rating_2
    dictionary["rating_1"] = int(rating_1.replace(",", "")) if rating_1 else rating_1

    return dictionary


def get_tech_info(soup, dictionary):
    date_updated = soup.find("div", {"itemprop": "datePublished"})
    num_installs = soup.find("div", {"itemprop": "numDownloads"})
    current_version = soup.find("div", {"itemprop": "softwareVersion"})
    android_versions = soup.find("div", {"itemprop": "operatingSystems"})
    content_rating = soup.find("div", {"itemprop": "contentRating"})

    dictionary["last_update"] = get_date(date_updated.string.strip()) if date_updated else date_updated
    dictionary["num_installs"] = num_installs.string.strip() if num_installs else num_installs
    dictionary["current_version"] = current_version.string.strip() if current_version else current_version
    dictionary["android_version"] = android_versions.string.strip() if android_versions else android_versions
    dictionary["content_rating"] = content_rating.string.strip() if content_rating else content_rating

    return dictionary


def is_dev_email(tag):
    if tag.has_attr("class") and tag.has_attr("href") and tag["href"].find("mailto") > -1:
        return True
    return False


def get_dev_info(soup, dictionary):
    dev = soup.find("a", {"class": "document-subtitle primary"}).span
    dev_mail = soup.find(is_dev_email)
    dev_address = soup.find("div", {"class": "content physical-address"})

    dictionary["dev_name"] = dev.string if dev else dev
    dictionary["dev_mail"] = dev_mail.string.replace("Email", "").strip() if dev_mail else dev_mail
    dictionary["dev_address"] = str(dev_address) if dev_address else dev_address

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
