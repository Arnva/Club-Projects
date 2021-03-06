'''
Covid-19 Statistics Tracker

Built by MNS 11-A CS Club

Requirements:
- Python3
- PySimpleGUI
- requests
'''

import requests
import PySimpleGUI as psg
import json

with open('settings.json') as f:
    settings = json.load(f) # Load settings.json
# PSG setup
psg.theme(settings['theme']) # Set theme to previously selected theme

api = 'https://corona.lmao.ninja/v2/countries/{country}?yesterday&strict&query' # WIP: Make User-settable

FIELDS = {'country': 'Country Name: ', 'cases': 'Cases: ', 'todayCases': 'Cases Today: ', 'deaths': 'Deaths: ', 'todayDeaths': 'Deaths Today: '} # WIP: Make User-settable

def get_results(c: str) -> str:
    '''Get API data for a country'''
    resp = requests.get(api.format(country=c))
    result = resp.json()
    if not result.get('message'):
        data = [f'{d}{result.get(f)}' for f, d in FIELDS.items()]
        return ', '.join(data)
    else:
        return 'No results found for this country!'


def load_tool() -> None:
    '''Load the Input window'''
    layout = [[psg.Text('Enter Country: ', key='search_txt'), psg.InputText(key='bar')], [psg.Button('Search', bind_return_key=True)]]
    window = psg.Window('COVID StatFinder', layout=layout)
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED:
            window.close()
            return None
        elif event == 'Search':
            window.close()
            return values
        else:
            return None


def load_results(values) -> None:
    '''Load Results screen'''
    result_layout = [[psg.Text(f'Results: {get_results(values["bar"])}')], [psg.Button('Close', bind_return_key=True)]]
    window = psg.Window('COVID StatFinder', layout=result_layout)
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED or event == 'Close':
            window.close()
            break
    load_home()


def load_settings() -> None:
    '''Load Settings screen'''
    rows = []
    i = [0, 15]
    while i[1] < len(psg.theme_list()):
        rows.append(psg.theme_list()[i[0]:i[1]])
        i[0], i[1] = i[1], i[1]+15

    settings_layout = [[psg.Text('Select theme: ')]]
    for row in rows:
        settings_layout.append([psg.Button(t) for t in row])
    settings_layout.append([psg.Button('Cancel')])
    window = psg.Window('COVID StatFinder', layout=settings_layout)
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED or event == 'Cancel':
            window.close()
            break
        elif event in [r for row in rows for r in row]:
            psg.theme(event)
            with open('settings.json', 'w') as f:
                json.dump({'theme': event}, f)
            break
    window.close()
    load_home()


def load_home() -> None:
    '''Load Home screen'''
    home_layout = [[psg.Text('COVID StatFinder')], [psg.Button('Settings'), psg.Button('Start')]]
    window = psg.Window('COVID StatFinder', layout=home_layout)
    while True:
        event, values = window.read()
        if event == 'Start':
            window.close()
            results = load_tool()
            if results:
                load_results(results)
            break
        elif event == 'Settings':
            window.close()
            load_settings()
            break
        elif event == psg.WIN_CLOSED:
            window.close()
            break

        
load_home() # Begin event loop