# Hall of Apps: The Top Android Apps Metadata Archive
| Resource | DOI |
|:---:|:---:|
|Dataset| [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3653367.svg)](https://doi.org/10.5281/zenodo.3653367)|

Hall-of-Apps is a dataset containing top charts’ apps metadata extracted (weekly) from GP, for 4 different countries, during 30 weeks.

The extraction process consist of the phases: Scrapping and HTML parsing.

1. **Google Play Scraping:** This phase consist of extracting the HTML representation of each app belonging to the top charts of a category and the Editor Choice List. To this, we created two NodeJS scripts: the first one in charge of extracting the list of apps in all the categories’ top chart, and the second one in charge of going through the aforementioned list with the purpose of extracting the associated HTML file for each element of the list.
2. **HTML Parsing:** This phase consist of extracting information from the HTML files. We developed an HTML parser written in Python (using BeautifulSoup library) to search the targeted tags and then extract its content, before being stored in a NoSQL database. 
3. **D3 Visualizations:** After storing the data into a NoSQL database and in order to facilitate the understanding of our dataset, we generated visualizations to explain some of the metrics, distributions and statistics of the data in the database. 

### Tools

This repository presents the tools used to extract, parse, store and visualize the dataset.

**Google Play Scraper** contains the NodeJS scripts used to extract the HTML files.


**HTML Parser** contains the parser to extract information from the HTML and store it into a MongoDB.


**D3 Visualizations** contains the JS scripts to generate the visualization presented in the online appendix.

### Dataset

Hall-of-Apps has two storage mechanisms:

1. The first one is raw HTML files; these files are stored by week and grouped by month. Each file has a predefined naming structure to identify the week date in which the apps were extracted, app package, country, collection (i.e., top free or top paid) and category.
> \<weekInterval>%\<collection>%\<category>%\<appPackage>.html

2. The second one is a NoSQL database, in particular, a MongoDB.

When uncompressed, Hall-of-Apps raw HTML files weights 231GB, thus, it was stored in a .tar.bz2 file with a smaller size of 38GB. 

Moreover, the MongoDB database was exported using *mongodump*, an utility for creating binaries of the contents, and compressed into a .zip file of size 3.2GB. Both formats were uploaded to Zenodo to enable further studies and analyzes and can be downloaded here: 

To restore the DB:

1. Install [MongoDB](https://docs.mongodb.com/manual/administration/install-community/)
2. Start MongoDB
3. Download the dataset from Zenodo
4. Unzip the mining file (mining.zip)
5. Execute command and wait until it finishes: 
> mongorestore -d mining \<path-mining-folder>
6. Execute command:
> mongo
7. To check existing DBs, execute and check if 'mining' appears:
> show dbs 
8. Switch to *mining* DB:
> use mining
9. List all collections for mining DB and check if *app*, *review* and *extra_app* collections appear:
> show collections

