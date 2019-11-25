from decimal import *


def get_apps(soup, class_content, dictionary, state):

    apps= []

    if soup.find("div", {"class": class_content}) is not None:
        apps = soup.find("div", {"class": class_content}).find_all("div", {"class": "card no-rationale square-cover apps small"})

    amount_apps = len(apps)
    dictionary[f'amount_{state}_apps'] = amount_apps
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


        #id_extra_apps = "N/A" if similar_id is None else similar_id
        current_app = {
                    "id":"N/A" if similar_id is None else similar_id,
                    "name": "N/A" if similar_name is None else similar_name.strip(),
                    "dev_name": "N/A" if similar_dev_name is None else similar_dev_name,
                    "price": "N/A" if price_button is None or price_button == "N/A" else price_button.span.string,
                    "summary": "N/A" if similar_description is None else similar_description.strip(),
                    "rating": -1.0 if similar_rating is None else float(round(Decimal(similar_rating.div["aria-label"].split("stars")[0].replace("Rated", "").strip()),3)),
                    "app_id": dictionary["_id"]["id"],
                    "app_retrieved_date_start": dictionary["_id"]["retrieved_date_start"],
                    "app_retrieved_date_end": dictionary["_id"]["retrieved_date_end"],
                    "app_name": dictionary["name"],
                    "app_id":dictionary["_id"]["id"],
                    "app_retrieved_date_start": dictionary["_id"]["retrieved_date_start"],
                    "app_retrieved_date_end":dictionary["_id"]["retrieved_date_end"],
                    #"_id": {}
                    }
                       
        #lau esto no se puede dado a que hay ids que son None entonces se repite muchas veses las posibles PK
        #current_app["_id"]["id"] = id_extra_apps
        #current_app["_id"]["app_retrieved_date_start"] = dictionary["_id"]["retrieved_date_start"]
        #current_app["_id"]["app_retrieved_date_end"] = dictionary["_id"]["retrieved_date_end"]

        data_apps.append(current_app)

    return dictionary, data_apps
