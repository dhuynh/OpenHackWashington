import PySimpleGUI as sg 

from flaskapp import classes
import sys
from pprint import pprint


#GUI
layout = [[sg.Text('Enter a Search Query', size = (30, 1)), sg.Text('Sort by (last_modified, size, filename, type):', size = (30, 1))],
          [sg.Input(do_not_clear=True, key='_query_', size = (40, 1)), sg.Input(do_not_clear=True, key='_sortby_', size = (30, 1))],
          [sg.Checkbox('Full Lucerne Search?', key='_lucerne_')],    
          [sg.Button('Query'), sg.Exit()],
          [sg.Text('Waiting for Query...')]]      

window = sg.Window('Azure Search', layout)

qb = classes.QueryBuilder()

if sys.argv[1] == "createskillset":
    qb.createskillset(sys.argv[2])


if sys.argv[1] == "hitsearch":
    while True:
        event, values = window.Read()
        if event is None or event == 'Exit':
            break
        else:
            if values['_lucerne_']:
                search_type = "full"
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

            documentsreturned = qb.hitsearch(values['_query_'], sortby, search_type)

            hits = "Number of Hits:" + str(len(documentsreturned))
            sg.Popup(documentsreturned, hits, search_type)
        print(event, values)

window.Close()