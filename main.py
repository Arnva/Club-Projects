import requests
import PySimpleGUI as psg
from requests.api import get

# PSG setup
psg.theme('DarkAmber')
layout = [[psg.Text('Enter Country: ', key='search_txt'), psg.InputText(key='bar')], [psg.Button('Search', bind_return_key=True)]]
window = psg.Window('COVID StatFinder', layout=layout)





api = 'https://corona.lmao.ninja/v2/countries/{country}?yesterday&strict&query' # Find suitable API today.

FIELDS = {'country': 'Country Name: ', 'cases': 'Cases: ', 'todayCases': 'Cases Today: ', 'deaths': 'Deaths: ', 'todayDeaths': 'Deaths Today: '}

def get_results(c):
    resp = requests.get(api.format(country=c))
    result = resp.json()
    if not result.get('message'):
        data = [f'{d}{result.get(f)}' for f, d in FIELDS.items()]
        return ', '.join(data)
    else:
        return 'No results found for this country!'


while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED or event == 'Search':# if user closes window or clicks cancel
        result_layout = [[psg.Text(f'Results: {get_results(values["bar"])}')]]
        window.close()
        window = psg.Window('COVID StatFinder', layout=result_layout)
        event, values = window.read()
        if event == psg.WIN_CLOSED:
            break