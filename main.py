import requests
import PySimpleGUI as psg
import json

with open('settings.json') as f:
    settings = json.load(f)
# PSG setup
psg.theme(settings['theme'])

api = 'https://corona.lmao.ninja/v2/countries/{country}?yesterday&strict&query'

FIELDS = {'country': 'Country Name: ', 'cases': 'Cases: ', 'todayCases': 'Cases Today: ', 'deaths': 'Deaths: ', 'todayDeaths': 'Deaths Today: '}

def get_results(c):
    resp = requests.get(api.format(country=c))
    result = resp.json()
    if not result.get('message'):
        data = [f'{d}{result.get(f)}' for f, d in FIELDS.items()]
        return ', '.join(data)
    else:
        return 'No results found for this country!'

def load_tool():
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

def load_results(values):
    result_layout = [[psg.Text(f'Results: {get_results(values["bar"])}')], [psg.Button('Close', bind_return_key=True)]]
    window = psg.Window('COVID StatFinder', layout=result_layout)
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED or event == 'Close':
            window.close()
            break

def load_settings():
    row1 = psg.theme_list()[:10]
    settings_layout = [[psg.Text('Select theme: ')], [psg.Button(theme) for theme in row1], [psg.Button('Cancel')]]
    window = psg.Window('COVID StatFinder', layout=settings_layout)
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED or event == 'Cancel':
            window.close()
            break
        elif event in row1:
            psg.theme(event)
            with open('settings.json', 'w') as f:
                json.dump({'theme': event}, f)
            break
    window.close()
    load_home()

def load_home():
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
load_home()