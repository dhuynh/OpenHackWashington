import requests
import json
import os
import sys
import simplejson
import pandas as pd
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

pd.set_option('display.max_colwidth', 300)
class QueryBuilder(object):
    def __init__(self):
        self.base_params = params
        self.headers = headers

    def hitsearch(self, query, sortby=None, query_type=None):
        update =  {"search": query}
        if query_type is not None:
            update.update({"queryType": query_type})
        if sortby is not None:
            update.update({"$orderby": sortby})

        # Full search if checkmark is typed
        url = baseurl + "indexes/azureblob-index/docs"
        self.base_params.update(update)
        payload = ""
        response = requests.get(url=url, data=payload, headers=self.headers, params=self.base_params)
        if response.status_code != 200:
            print("error parsing the response: %s" % str(response.content))
            return pd.DataFrame([])
        payload = json.loads(response.text)['value']
        filenames = []
        for documents in payload:
            filenames.append({"name": documents['metadata_storage_name'],
                              "modified": documents["metadata_storage_last_modified"],
                              "image_tags": documents["tags"],
                              "categories": documents["categories"],
                              "sentiment": documents["sentiment"],
                              "url": documents["url"],
                              "organization": documents["organization"],
                              "person": documents["person"],
                              "location": documents["location"],
                              "summary": documents["keyPhrases"]})

        df = pd.DataFrame(filenames)
        df["sentiment"] = df["sentiment"].astype(float)
        df["categories"] = df["categories"].astype(str)
        df = df.round({"sentiment": 2})
        # styles = [
        #     dict(
        #         props=[
        #             ('border-collapse', 'separate'),
        #             ('border-spacing', '10px 50px')
        #         ]
        #     ),
        #     dict(
        #         selector="thead",
        #         props=[('display', 'none')]
        #     )
        # ]
        #
        # df.style.set_properties(subset=df.columns[[0, 2]], **{'text-align': 'right'}) \
        #     .set_properties(subset=df.columns[[1, 3]], **{'text-align': 'left'}) \
        #     .set_table_styles(styles)
        return df

class ConfigManager(object):
    def __init__(self, config_path):
        self.base_params = params
        self.headers = headers
        self.config_path = config_path
        self.index_path = os.path.join(self.config_path, "index_config.json")
        self.skillset_path = os.path.join(self.config_path, "skillset_config.json")
        self.indexer_path = os.path.join(self.config_path, "skillset_config.json")

    def delete_index(self):
        r = requests.delete(url=baseurl + "indexes/azureblob-index", headers=headers, params=self.base_params)
        print(r.status_code)

    def get_index(self):
        r = requests.get(url=baseurl + "indexes/azureblob-index", headers=headers, params=self.base_params)
        config = r.content
        print(r.status_code)
        if len(config) < 5:
            print("nothing to write")
            sys.exit(0)
        outfile = open(self.index_path, "w")
        outfile.write(simplejson.dumps(simplejson.loads(config), indent=4, sort_keys=True))

    def post_index(self):
        with open(self.index_path) as outfile:
            config = json.load(outfile)
        r = requests.post(url=baseurl + "indexes", headers=headers, json=config, params=self.base_params)
        print(r.status_code)

    def create_skillset(self, skillsetname):
        payload = ""
        with open(self.skillset_path) as config:
            config = json.load(config)
        print(baseurl + "skillsets/" + skillsetname)
        response = requests.put(url = baseurl + "skillsets/" + skillsetname, data=payload, headers=self.headers,
                                params=self.base_params, json=config)
        if response.status_code != 201:
            print("error parsing the response: %s" % str(response.content))
            return {}
        payload = json.loads(response.text)
        return payload
