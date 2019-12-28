from decimal import *


def get_apps(soup, class_content, dictionary, state, is_new_page):

    apps = []

    if soup.find("div", {"class": class_content}) is not None:
        apps = soup.find("div", {"class": class_content}).find_all("div", {"class": "card no-rationale square-cover apps small"})

    amount_apps = len(apps)

    if is_new_page and amount_apps == 0:
        amount_apps = None

    dictionary[f'amount_{state}_apps'] = amount_apps
    data_apps = []

    for app in apps:
        similar_id = app["data-docid"]
        similar_name = app.find("a", {"class": "title"}).get_text()
        similar_dev_info = app.find("div", {"class": "subtitle-container"})
        similar_dev_name = similar_dev_info.a
        similar_price = similar_dev_info.span.find("span", {"data-docid": similar_id})
        price_button = similar_price.button if similar_price else similar_price

        similar_description = app.find("div", {"class": "description"}).get_text()
        similar_rating = app.div.find("div", {"class": "reason-set"}).span.a.div

        id_extra_app = similar_id

        current_app = {
                    "name": similar_name.strip() if similar_name else similar_name,
                    "dev_name": similar_dev_name.string.strip() if similar_dev_name else similar_dev_name,
                    "price": price_button.span.string if price_button else price_button,
                    "summary": similar_description.strip() if similar_description else similar_description,
                    "rating": float(round(Decimal(similar_rating.div["aria-label"].split("stars")[0].replace("Rated", "").strip()), 3)) if similar_rating else similar_rating,
                    "app_name": dictionary["name"],
                    "id": id_extra_app,
                    "state": state,
                    "app_id": dictionary["id"],
                    "app_retrieved_date_start": dictionary["retrieved_date_start"],
                    "app_retrieved_date_end": dictionary["retrieved_date_end"],
                    "category": dictionary["category"],
                    "country": dictionary["country"]
                    }

        data_apps.append(current_app)

    return dictionary, data_apps
