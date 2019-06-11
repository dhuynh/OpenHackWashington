import requests
import json

url = "https://duyssearch.search.windows.net/indexes/azureblob-index/docs"

querystring = {"api-version":"2019-05-06","search":"New York"}

payload = ""
headers = {
    'Content-Type': "application/json",
    'api-key': "310C82B26640CFDBF100D8561EF5065D",
    'cache-control': "no-cache",
    'Postman-Token': "08038873-6b32-4f6b-bc7a-0a1d9a670a2e"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

payload = json.loads(response.text)['value']

filenames = []
for documents in payload:
    filenames.append(documents['metadata_storage_name'])
print(filenames)