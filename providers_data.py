import sqlite3
import pandas as pd
import requests
import json
import io

# URL for listing datasets
dataset_url = 'https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items'
headers = {'accept': 'application/json'}

# Make a request to get all datasets
response = requests.get(dataset_url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    data = response.json()

    # Initialize variables
    download_url = None

    # Iterate over all items and look for identifier = "6jpm-sxkc", which is the "Home Health Care Agencies" dataset
    for item in data:
        identifier = item.get("identifier")
        if identifier == "6jpm-sxkc":
            # Get the download URL from the distribution
            distribution = item.get("distribution", [])
            download_url = next((dist.get("downloadURL") for dist in distribution if dist.get("downloadURL")), None)
            break

    # If the download URL was found, proceed with downloading the CSV
    if download_url:
        print(f"Download URL found: {download_url}")

        # Download the CSV file
        csv_response = requests.get(download_url)
        if csv_response.status_code == 200:
            print("CSV file downloaded successfully.")
        else:
            print(f"Failed to download CSV file. Status code: {csv_response.status_code}")
            exit()

        # Load the CSV into a pandas DataFrame
        csv_data = pd.read_csv(io.StringIO(csv_response.text))

        # Create a SQLite database connection
        conn = sqlite3.connect('providers_data.db')

        # Insert the DataFrame into a SQLite table
        csv_data.to_sql('providers', conn, if_exists='replace', index=False)

        # Confirm data has been written
        print("CSV data successfully inserted into SQLite database.")

        # Close the connection
        conn.close()

    else:
        print("No download URL found for the specified identifier.")
else:
    print(f"Failed to retrieve datasets. Status code: {response.status_code}")
