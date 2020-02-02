from decimal import *
import json
import re

def script_in_text(id_tag=False,key='ds:4'):

    def regex_f(tag):

        return tag.name == 'script' and key in tag.get_text() and 'return' in tag.get_text() 

    def regex_id(tag):

        return tag.name == 'script' and '1.39809457E8' in tag.get_text() 

    function = regex_id if id_tag else regex_f
    
    return function

def get_key_apps(soup, type_extra='similar'):

    script = soup.find_all(script_in_text(True))
    txt_id_apps = script[0].get_text()
    key = None

    id_tag= '1.39809457E8' if type_extra == 'similar' else '1.62435799E8' #  change this for more developers

    try:
        line_key = re.search(f'.*{id_tag}.*\n', txt_id_apps).group(0)

        if 'ds:4' in line_key and type_extra == 'similar':
            key=  'ds:4'
        elif 'ds:5' in line_key and type_extra == 'similar':
            key = 'ds:5'

    except Exception as e:
        pass

    return key

def get_field_app(field, extra_app):


    try:
        if field=='name':
            response=extra_app[2]

        elif field=='dev_name':
            response=extra_app[4][0][0][0]

        elif field=='summary':
            response=extra_app[4][1][1][1][1]

        elif field=='rating':
            response=float(extra_app[6][0][2][1][0])

        elif field=='id':
            response= extra_app[7][0][3][3][0]            

        elif field=='price':
            response= extra_app[7][0][3][2][1][0][0]

        elif field=='currency':
            response= extra_app[7][0][3][2][1][0][1]
    except Exception as e:
        print(e, field)
        print(extra_app)
        response = None
    return response

def get_new_extra_similar(soup, dictionary):

    key = get_key_apps(soup)

    data_apps = []


    if key is not None:

        #info apps
        script = soup.find_all(script_in_text(False,key)) 
        text_script = script[0].get_text() # text for script tag
        info_extra_apps = text_script[text_script.find("return")+7:text_script.find("}});")] # finds return and locates array apps
        info_extra_apps = json.loads(info_extra_apps)
        

        try:
            for app in info_extra_apps[1][1][0][0][0][0]:
                current_app = {
                # info from extra app
                "name": get_field_app('name',app),
                "dev_name": get_field_app('dev_name',app),
                "price": "Free" if get_field_app('price',app) == 0 else get_field_app('price',app),
                "currency":get_field_app('currency',app),
                "summary": get_field_app('summary',app),
                "rating": get_field_app('rating',app),
                "id": get_field_app('id',app),
                #general extra app
                "state": 'similar',
                #data from app
                "app_id": dictionary["id"],
                "app_retrieved_date_start": dictionary["retrieved_date_start"],
                "app_retrieved_date_end": dictionary["retrieved_date_end"],
                "category": dictionary["category"],
                "country": dictionary["country"],            
                "app_name": dictionary["name"],
                }

                data_apps.append(current_app)

        except Exception  as e:
            print(e)
            pass

    return data_apps



def get_apps(soup, class_content, dictionary, state, is_new_page):

    apps = []

    if soup.find("div", {"class": class_content}) is not None:
        apps = soup.find("div", {"class": class_content}).find_all("div", {"class": "card no-rationale square-cover apps small"})

    amount_apps = len(apps)

    if is_new_page and amount_apps == 0:
        amount_apps = 0

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

    if is_new_page:
        new_extra_app = get_new_extra_similar(soup, dictionary) if state == 'similar' else [] 
        dictionary[f'amount_{state}_apps'] = dictionary[f'amount_{state}_apps']  + len(new_extra_app)
        data_apps.extend(new_extra_app)

    return dictionary, data_apps
