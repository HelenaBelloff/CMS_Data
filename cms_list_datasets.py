import requests
import json

# URL for the dataset items via the CMS API
url = 'https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items' 
headers = {'accept': 'application/json'}

# Make a request to get all datasets
response = requests.get(url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    data = response.json()

    # Create a list to hold all the dataset information
    datasets_info = []
    multiple_download_urls = []  # List to track datasets with more than one downloadURL (not sure if this is ever a case, but we'll catch it regardless)


    # Iterate over all items and extract the desired fields
    for item in data:
        title = item.get("title")
        identifier = item.get("identifier")
        description = item.get("description")
        distribution = item.get("distribution", [])

         # Find all download URLs (if there are multiple)
        download_urls = [dist.get("downloadURL") for dist in distribution if dist.get("downloadURL")]
        # Check if there is more than one download URL
        if len(download_urls) > 1:
            multiple_download_urls.append({
                "title": title,
                "identifier": identifier,
                "downloadURLs": download_urls
            })

        # Store only the first download URL in the dataset info (just for simplicity right now)
        download_url = download_urls[0] if download_urls else None

        # If we assumed there is always at least one URL and we only cared about that one, we could just use the following line instead.
        # download_url = distribution[0].get("downloadURL") if distribution else None

        # Store the relevant info in a dictionary
        dataset_info = {
            "title": title,
            "identifier": identifier,
            "description": description,
            "downloadURL": download_url
        }

        # Add the dataset info to the list
        datasets_info.append(dataset_info)

    # Save the collected datasets info to a new JSON file
    with open('CMS_datasets_list.json', 'w') as json_file:
        json.dump(datasets_info, json_file, indent=4)

    # If there are datasets with multiple download URLs, save them to a separate JSON file
    if multiple_download_urls:
        with open('CMS_datasets_with_multiple_download_urls.json', 'w') as json_file:
            json.dump(multiple_download_urls, json_file, indent=4)

        # I like when it talks to me... 
        print(f"Found datasets with multiple download URLs. Saved them to 'CMS_datasets_with_multiple_download_urls.json'.")
    else:
        print("No datasets with multiple download URLs found.")

    print(f"Successfully saved dataset information to 'CMS_datasets_list.json'.")

else:
    print(f"Failed to retrieve datasets. Status code: {response.status_code}")
