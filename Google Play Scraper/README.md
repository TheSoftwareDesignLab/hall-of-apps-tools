# Google Play Scraper

Our Scrapper consist of two scripts. The first one, in charge of listing the urls that must be visited, and the second one in charge of extracting the apps information from each url previously listed.

In order to run the first script you will need to run the command:
```sh
node index.js
```
This script will generate a json containing the list of apps belonging to the top charts for each country and each category. This file is stored inside a folder called ```results``` and its file name contains the starting and ending date of the week the script was executed. Finnaluy

The second script reads the json file previously created and for each url visits it and extract the information of the app asociated to the url. In order to execute itr you have tio run:
```sh
$ node retrieveData.js
```
