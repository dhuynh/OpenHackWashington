import PySimpleGUI as sg 
import requests
import json
import sys
from pprint import pprint
url = "https://duyssearch.search.windows.net/indexes/azureblob-index/docs"     

#GUI
layout = [[sg.Text('Enter a Search Query', size = (30, 1)), sg.Text('Sort by (last_modified, size, filename, type):', size = (30, 1))],
          [sg.Input(do_not_clear=True, key='_query_', size = (40, 1)), sg.Input(do_not_clear=True, key='_sortby_', size = (30, 1))],
          [sg.Checkbox('Full Lucerne Search?', key='_lucerne_')],    
          [sg.Button('Query'), sg.Exit()],
          [sg.Text('Waiting for Query...')]]      

window = sg.Window('Azure Search', layout)

class QueryBuilder(object):
    def __init__(self, query_type=None):

        if query_type is None:
            self.base = {
                "api-version": "2019-05-06"
            }
        else:
            self.base = {
                "api-version": "2019-05-06",
                "queryType": query_type
            }
        self.headers = {
            'Content-Type': "application/json",
            'api-key': "310C82B26640CFDBF100D8561EF5065D",
            'cache-control': "no-cache",
            'Postman-Token': "08038873-6b32-4f6b-bc7a-0a1d9a670a2e"
        }

    def hitsearch(self, query, sortby):
        # Full search if checkmark is typed
        self.base.update({"search": query, "$orderby": sortby})
        payload = ""
        response = requests.get(url=url, data=payload, headers=self.headers, params=self.base)
        payload = json.loads(response.text)['value']
        pprint(payload)
        filenames = []
        for documents in payload:
            filenames.append({documents['metadata_storage_name'], documents["metadata_storage_last_modified"], documents["metadata_storage_size"]})
        return filenames


if sys.argv[1] == "hitsearch":
    while True:
        event, values = window.Read()
        if event is None or event == 'Exit':
            break
        else:
            if values['_lucerne_']:
                search_type = "Full"
            else:
                search_type = None
            sortby=None
            if values['_sortby_'] == "last_modified":
                sortby="metadata_storage_last_modified desc"
            elif values['_sortby_'] == "filename":
                sortby = "metadata_storage_name"
            elif values['_sortby_'] == "size":
                sortby = "metadata_storage_size"
            elif values['_sortby_'] == "type":
                sortby = "metadata_storage_content_type"

            qb = QueryBuilder(search_type)
            documentsreturned = qb.hitsearch(values['_query_'], sortby)

            hits = "Number of Hits:" + str(len(documentsreturned))
            sg.Popup(documentsreturned, hits, search_type)
        print(event, values)

window.Close()