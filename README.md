# CMS Data
The following scripts interact with the Centers for Medicare & Medicaid Services API. Normally, I'd list prereqs in here, etc., but I'm already going overboard :D

## 1. Listing the CMS datasets
The ```cms_list_datasets.py``` file will return a JSON file that lists all of the datasets from [CMS Provider Dataset API](https://data.cms.gov/provider-data/) so you can get a clear view of what's in there.

## 2. Inserting a dataset into a SQLite db 

The ```providers_data.py``` file will make a request to get this same list of datasets. Then, it looks for the ```download_url``` where the ```identifier == "6jpm-sxkc"```, which corresponds to the [Home Health Care Agencies dataset](https://data.cms.gov/provider-data/dataset/6jpm-sxkc). It will save the CSV in a pandas df and then create a sqlite db called ```providers_data.db```. From there, the script inserts the pandas df into the sqlite db and calls the table ```providers```.

## 3. Testing
The ```test.py``` file just tests that the ```providers``` table made it into ```providers_data.db``` by querying a few rows. You don't actually need this script, though. You can just run:

```bash
sqlite3 providers_data.db 
```
and then 

```sql
SELECT * FROM providers limit 10;
```
