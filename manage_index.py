import requests
import sys
import json
import simplejson

headers = {

            'Content-Type': "application/json",
            'api-key': "310C82B26640CFDBF100D8561EF5065D",
            'cache-control': "no-cache",
            'Postman-Token': "08038873-6b32-4f6b-bc7a-0a1d9a670a2e"

}
params = {
            "api-version": "2019-05-06"
        }
if sys.argv[1] == "delete":
    requests.delete(url="https://duyssearch.search.windows.net/indexes/azureblob-index", headers=headers, params=params)

if sys.argv[1] == "get":
    r = requests.get(url="https://duyssearch.search.windows.net/indexes/azureblob-index", headers=headers, params=params)
    config = r.content
    print(r.status_code)
    if len(config) < 5:
        print("nothing to write")
        sys.exit(0)
    outfile = open("index_config.json", "w")
    outfile.write(simplejson.dumps(simplejson.loads(config), indent=4, sort_keys=True))

if sys.argv[1] == "post":
    with open('index_config.json', 'r') as outfile:
        config = json.load(outfile)["fields"]
    r = requests.post(url="https://duyssearch.search.windows.net/indexes", headers=headers, json=config, params=params)
