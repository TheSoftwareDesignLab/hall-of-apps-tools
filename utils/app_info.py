from decimal import *


def get_basic_info(soup, file, dictionary):

    app_id = soup.find("div", {"class": "details-wrapper apps"})
    app_name = soup.find("div", {"class": "id-app-title"})
    app_description = soup.find("meta", {"name": "description"})
    app_url = soup.find("meta", {"property": "og:url"})
    genre = soup.find("a", {"class": "document-subtitle category"}).span
    price = soup.find("meta", {"itemprop": "price"})
    description = soup.find("div", {"class": "show-more-content text-body", "itemprop": "description"}).get_text()

    file_info = file.split("%")
    retrieved_date = file_info[0]
    country = file_info[1]
    category = file_info[2]

    dictionary["id"] = "N/A" if app_id is None else app_id["data-docid"].strip()
    dictionary["name"] = "N/A" if app_name is None else app_name.string.strip()
    dictionary["summary"] = "N/A" if app_description is None else app_description["content"].strip()
    dictionary["url"] = "N/A" if app_url is None else app_url["content"].strip()
    dictionary["category"] = "N/A" if category is None else category
    dictionary["country"] = "N/A" if country is None else country
    dictionary["retrieved_date"] = "N/A" if retrieved_date is None else retrieved_date
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

    dictionary["rating"] = 0 if rating is None else float(round(Decimal(rating["content"]), 3))
    dictionary["rating_5"] = 0 if rating_5 is None else int(rating_5.replace(",", ""))
    dictionary["rating_4"] = 0 if rating_4 is None else int(rating_4.replace(",", ""))
    dictionary["rating_3"] = 0 if rating_3 is None else int(rating_3.replace(",", ""))
    dictionary["rating_2"] = 0 if rating_2 is None else int(rating_2.replace(",", ""))
    dictionary["rating_1"] = 0 if rating_1 is None else int(rating_1.replace(",", ""))

    return dictionary


def get_tech_info(soup, dictionary):
    date_updated = soup.find("div", {"itemprop": "datePublished"})
    num_installs = soup.find("div", {"itemprop": "numDownloads"})
    current_version = soup.find("div", {"itemprop": "softwareVersion"})
    android_versions = soup.find("div", {"itemprop": "operatingSystems"})
    content_rating = soup.find("div", {"itemprop": "contentRating"})

    dictionary["last_update"] = "N/A" if date_updated is None else date_updated.string.strip()
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