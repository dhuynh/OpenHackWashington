import PySimpleGUI as sg 
import requests
import json

url = "https://duyssearch.search.windows.net/indexes/azureblob-index/docs"     

#GUI
layout = [[sg.Text('Enter a Search Query')],      
          [sg.Input(do_not_clear=True, key='_query_')],  
          [sg.Checkbox('Full Lucerne Search?', key='_lucerne_')],    
          [sg.Button('Query'), sg.Exit()],
          [sg.Text('Waiting for Query...')]]      

window = sg.Window('Azure Search', layout)

def hitsearch(query):
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
    return filenames

while True:      
    event, values = window.Read()
    if event is None or event == 'Exit':      
        break
    else:
        if values['_lucerne_']:
            lucerne = True
            documentsreturned = hitsearch(values['_query_'])
        else:
            lucerne = False
            documentsreturned = hitsearch(values['_query_'])
        
        hits = "Number of Hits:" + str(len(documentsreturned)) 
        sg.Popup(documentsreturned, hits, lucerne)     
    print(event, values)




window.Close()