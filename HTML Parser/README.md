# HTML Parser

This parser extracts app metadata from raw HTML files to insert it in a MongoDB. To run it:

1. Download the raw HTML files from the dataset.
2. Install and start [MongoDB](https://docs.mongodb.com/manual/administration/install-community/)
3. Create a new database using:
```sh
use mining
```
3. Use this command to run the parser replacing *<path_to_folder_with_raw_htmls>* with the folder where all the folders of HTML files are stored.
```sh
python source.py <path_to_folder_with_raw_htmls>
```
Note: 
- If you want to ignore some folder, add its name to the *ignore_folders* array in *source.py*.
- Take into account that processing one folder takes around 4 hours.
