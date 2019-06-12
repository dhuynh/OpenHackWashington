import requests
import json
import os
import sys
import simplejson

baseurl = "https://duyssearch.search.windows.net/"
headers = {

            'Content-Type': "application/json",
            'api-key': "310C82B26640CFDBF100D8561EF5065D",
            'cache-control': "no-cache",
            'Postman-Token': "08038873-6b32-4f6b-bc7a-0a1d9a670a2e"

}
params = {
            "api-version": "2019-05-06"
        }


class QueryBuilder(object):
    def __init__(self, query_type=None):
        self.base_params = params
        self.headers = headers

    def hitsearch(self, query, sortby, query_type):
        # Full search if checkmark is typed
        url = baseurl + "indexes/azureblob-index/docs"
        self.base_params.update({"queryType": query_type, "search": query, "$orderby": sortby})
        payload = ""
        response = requests.get(url=url, data=payload, headers=self.headers, params=self.base_params)
        if response.status_code != 200:
            print("error parsing the response: %s" % str(response.content))
            return {}
        payload = json.loads(response.text)['value']
        filenames = []
        for documents in payload:
            filenames.append({"name": documents['metadata_storage_name'],
                              "modified": documents["metadata_storage_last_modified"],
                              "size": documents["metadata_storage_size"]})
        return filenames

    def createskillset(self, skillsetname, config_path):
        url = str(baseurl + "skillsets/" + skillsetname)
        payload = ""
        with open(os.path.join(config_path, "skillset_config")) as config:
            config = json.load(config)
        response = requests.put(url=url, data=payload, headers=self.headers, params=self.base_params, json=config)
        if response.status_code != 201:
            print("error parsing the response: %s" % str(response.content))
            return {}
        payload = json.loads(response.text)
        return payload

class ConfigManager(object):
    def __init__(self, config_path):
        self.base_params = params
        self.headers = headers
        self.config_path = config_path

    def delete_config(self, url):
        print(url)
        requests.delete(url=url, headers=headers, params=self.base_params)

    def get_config(self, url):
        r = requests.get(url=url, headers=headers, params=self.base_params)
        config = r.content
        print(r.status_code)
        if len(config) < 5:
            print("nothing to write")
            sys.exit(0)
        outfile = open(self.config_path, "w")
        outfile.write(simplejson.dumps(simplejson.loads(config), indent=4, sort_keys=True))

    def post_config(self, url):
        with open(self.config_path, 'r') as outfile:
            config = json.load(outfile)["fields"]
        r = requests.post(url=url, headers=headers, json=config, params=self.base_params)


