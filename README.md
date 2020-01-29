
## Publications
<p align="justify">
Coming Soon!
</p>

## Technologies
<p align="justify">
To generate the Hall-of-Apps, we used the process below to extract, parse, store and visualize the data:
</p>

![Coming Soon](/assets/imgs/structural/coming_soon.png)

### Google Play Scrapper
<p align="justify">
  To achieve the first part, we used a scraper written in <strong>BlaBlaBla</strong> which generated HTMLs files with the metadata of apps released in the Google Play Store.
  <!--TODO: esperar a que la sección del scraper esté lista para mencionar las tecnologías y también las horas y días a las que se ejecutaba-->  
</p>

### HTML Parser
<p align="justify">
  In addition to the <i>Google Play Scrapper</i>, we developed tool to parse the data in the HTML archives that were collected. For that, it was necessary to do a manual analysis of the HTML files to identify the tags, along with the classes names and identifiers, that contained relevant information and their corresponding data types.
</p>

<p align="justify">
  The parser is written in <strong>Python</strong> using the library <i>Beautiful Soup</i> to search tags and extract its content, in order to store it in a a non-relational database.
</p>

#### Dicoveries

* After parsing the files, we discovered that the HTML format from weeks 17 to 30, changed. Because of that, several records had null values because its content were stored in different tags. Additionally, the information related to  <i>reviews</i>, <i>developer replies</i>, <i>similar apps</i>, and <i>more apps from developer</i> ended up being obfuscated in the new format and, as a result, <strong>those 14 weeks don't have that information</strong>.
* As well, some categorical values changed, such as number of installations and android versions, which had more than 50 different categories. Because of that, we made the desitionto create new categories to homogenize the data and decrease the amount of categories.
* Depending of the country, each app had different currency, which makes the price comparrison infeasible. Thus, we calculated the price in dollars and added a new column with the calculated price.

## Dataset: Hall-of-Apps
<p align="justify">
  The resulting dataset is stored with two main components. The first one, which contains the raw HTML files of over 30 weeks, stores those files by week and grouped by month. Each file has a taxonomy to identify the week date in which the apps were extracted, app id, country, top and category where it belongs.
</p>

<p align="justify">
  The second component, contains the information extracted from the HTML files via the <i>developed parser</i>. That processed information was then used to populate a non-relational database, in this case, a MongoDB. We decided to use a non relational database due to the huge amount of raw files we had and taking into account not all apps contain the same information.
</p>

### Database Structure

![Non-relational database diagram.](/assets/imgs/structural/coming_soon.png)

<p align="justify">
  As shown in the image above, the database consists of three collections. The main collection is called <i><strong>app</strong></i> because it keeps characteristic information about the app and retrieval dates. However, each app could also have <i>reviews</i>, <i>similar apps</i>, and <i>more apps from the same developer</i>, thus, in order to prevent overloading the collection and to make easy to query information about reviews and extra apps, we created two new collections, <i><strong>review</strong></i> and <i><strong>extra app</strong></i>. 
</p>

<p align="justify">
  <i><strong>Review</strong></i> has information about the user who wrote the review, rating, date and, if the developer wrote a response, it also has the text and date. On the other hand, <i><strong>extra app</strong></i> has information about similar apps and more from developer. To distinguish the group where it belongs, each document has an <i>state</i> attribute which indicates if the app  is a similar app or more from developer app.
</p>

### Visualizations Scripts
<p align="justify">
  Finally, in order to facilitate the understanding of our dataset, we generated some visualizations, as shown inside this web page, that aim to explain some of the metrics, distributions and statistics of the data in the non-relational database.
</p>
<p align="justify">
  The scripts used to generate the visualizations are written in <strong>JavaScript</strong> using the library <i>Data Driven Documents</i>, or <i>D3</i>, to generate custom charts and diagrams. In detail, each of the scripts contains a function that generates a particular chart/visualization (for example, a Stacked Bar Chart) using as input CSV files that contain synthesized information of various aggregations and/or queries made in the non-relational database.
</p>

### Links
<p align="justify">
  The tools that were used to extract, parse and visualize the collected data can be found in the following [GitHub Repository](https://github.com/TheSoftwareDesignLab/hall-of-apps-tools)
</p>

## Metrics and Statistics
<p align="justify">
  As we explained previously, our dataset is composed of to components: The first one contains raw HTML files stored week by week over 30 weeks, and the second one is a non-relational database with all the processed information. The following figure depicts the amount of apps metadata extracted from the Google Play Store, grouped by month and subdividing it by country:
</p><br/>

<input type="checkbox" id="chartCountriessort">	Toggle sort 
<svg id="chartCountries" width="500" height="450"></svg>

<p align="justify">
  <small>
    The following chart aims to describe the total number of applications in our dataset, per month, as well as the distribution per <i>Country</i> in each month.
  </small>
</p><br/>

### General Discoveries
<p align="justify">
  Furthermore, it's worth noting that we extracted the best apps of the Google Play Store, thus, our non-relational database contains the <i>top free</i> and <i>top selling</i> apps for each category, as well as the <i>editors choice</i> in each country:
</p><br/>

Select Input <select id="chartTopsxaxis"></select>
<input type="checkbox" id="chartTopssort">	Toggle sort 
<svg id="chartTops" width="500" height="600"></svg>

<p align="justify">
  <small>
    The following chart aims to describe the total number of applications in our dataset per month, as well as the distribution per <i>Category</i> in each month, filtering by <i>tops</i> that were described previously.
  </small>
</p>

<p align="justify">
  The figure above shows that our dataset contains 33 differents app <i>categories</i>. In order to ease the global analysis of the apps in the non-relational database, we added to the <i><strong>app</strong></i> collectiona new attribute containing a <i>macro category</i>. These new <i>macro categories</i> were generated by grouping the original categories by their similarity. The following table depicts the new <i>macro categories</i>, and the figure below it aims to describe the total number of applications in our dataset per month, as well as the subdividing it by _ Macro Categories_ in each month, filtering by <i>tops</i>
</p><br/>

Select Input <select id="chartCustomCatxaxis"></select>
<input type="checkbox" id="chartCustomCatsort">	Toggle sort 
<svg id="chartCustomCat" width="500" height="620"></svg>

<p align="justify">
  As the previous figures show, it's possible to evidence a significant change in the total amount of collected apps regarding the Editors Choice since February of 2018. After a intense manual examination of the collected HTML files, we concluded that this disparity/drop amongst the monthly number Editors Choice apps was due to some external factors during the <i>scrapping phase</i>. For further details in the matter, please  refer to the subchapter <i>Banned IP</i> of the section <strong><i>Limitations and Challenges</i></strong> from the published paper (see <a href="#publications">Publications</a>). 
</p>

### App Collection Discoveries
<p align="justify">
  This collection has <strong>YYY</strong> records and a total of <strong>36</strong> attributes. The following figure depicts the attributes data-type distribution.  
</p>

Select Input <select id="chartTypesAppxaxis"></select>
<svg id="chartTypesApp" width="500" height="450"></svg>

<p align="justify">
  As the figure shows, the <i>String</i> data-type is predominant in this collection, folowed by <i>Numeric</i> attributes. In the same way, it's possible to evidence the same proportions when lookin at each individual country.
</p>

<p align="justify">
  In addition to the above, the table below shows in detail the data types of each of the attributes of the collection, as well as the percentage of null values
</p>


| Atribute Name | Type| % Null Values | Predominant Values |
| :-------------: | :----------: | :-----------: | :-----------: |
| _id | Object | 0% | N/A |
| amount_more_from_developer_apps | Numeric | 35.5% | 0 (~32.5%), 16 (~24%)
| amount_reviews | Numeric | 64.5% | 38 (~64%) |
| amount_similar_apps | Numeric | 35.5% | 18 (~64%), 16 (~27%) |
| android_version | String | 0.3% | "4.1 and up" (~21%), "4.0.3 and up" (~15%) |
| category | String | 0% | "music_and_audio" (~) |
| content_rating | String | 0% |  |
| country | String | 0% |  |
| currency | String | 0% |  |
| current_version | String | 2.4% |  |
| description | String | 0% |  |
| dev_address | String | 54% |  |
| dev_mail | String | 0% |  |
| dev_name | String | 0% |  |
| genre | Array | 0% |  |
| has_specific_version | Bool | 0% |  |
| has_whats_new | Bool | 0% |  |
| id | String | 0% |  |
| last_update | Date | 0% |  |
| name | String | 0% |  |
| num_installs | String | 0% |  |
| price | Numeric | 0% |  |
| price_usd | Numeric | 0% |  |
| rating | Numeric | 1.7% |  |
| rating_1 | Numeric | 23.8% |  |
| rating_2 | Numeric | 23% |  |
| rating_3 | Numeric | 22.4% |  |
| rating_4 | Numeric | 21.9% |  |
| rating_5 | Numeric | 21.5% |  |
| required_version | String | 0% |  |
| retrieved_date_end | Date | 0% |  |
| retrieved_date_start | Date | 0% |  |
| summary | String | 0% |  |
| top | String | 0% |  |
| url | String | 0% |  |
| whats_new | Array | 0% |  |

### Review Collection Discoveries

Select Input <select id="chartTypesReviewxaxis"></select>
<svg id="chartTypesReview" width="500" height="450"></svg>

### Extra App Collection Discoveries

Select Input <select id="chartTypesExtraxaxis"></select>
<svg id="chartTypesExtra" width="500" height="450"></svg>