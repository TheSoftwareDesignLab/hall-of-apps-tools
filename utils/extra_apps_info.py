from decimal import *


def get_apps(soup, class_content, dictionary, state):
    if soup.find("div", {"class": class_content}) is not None:
        apps = soup.find("div", {"class": class_content}).find_all("div", {"class": "card no-rationale square-cover apps small"})
    else:
        apps = []
    amount_apps = len(apps)
    dictionary["amount_%s_apps" % state] = amount_apps
    data_apps = []

    for app in apps:
        similar_id = app["data-docid"]
        similar_name = app.find("a", {"class": "title"}).get_text()
        similar_dev_info = app.find("div", {"class": "subtitle-container"})
        similar_dev_name = similar_dev_info.a.string.strip()
        similar_price = similar_dev_info.span.find("span", {"data-docid": similar_id})
        price_button = "N/A" if similar_price is None else similar_price.button

        similar_description = app.find("div", {"class": "description"}).get_text()
        similar_rating = app.div.find("div", {"class": "reason-set"}).span.a.div

        current_app = {"id": "N/A" if similar_id is None else similar_id,
                       "name": "N/A" if similar_name is None else similar_name.strip(),
                       "dev_name": "N/A" if similar_dev_name is None else similar_dev_name,
                       "price": "N/A" if price_button is None or price_button == "N/A" else price_button.span.string,
                       "summary": "N/A" if similar_description is None else similar_description.strip(),
                       "rating": -1.0 if similar_rating is None else float(round(Decimal(similar_rating.div["aria-label"].split("stars")[0].replace("Rated", "").strip()),3)),
                       "app_id": dictionary["id"],
                       "app_retrieved_date_start": dictionary["retrieved_date_start"],
                       "app_retrieved_date_end": dictionary["retrieved_date_end"],
                       "app_name": dictionary["name"]
                       }

        data_apps.append(current_app)

    return dictionary, data_apps
