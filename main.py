import requests
country = input('Enter country: ')
api = f'https://corona.lmao.ninja/v2/countries/{country}?yesterday&strict&query' # Find suitable API today.

FIELDS = {'country': 'Country Name: ', 'cases': 'Cases: ', 'todayCases': 'Cases Today: ', 'deaths': 'Deaths: ', 'todayDeaths': 'Deaths Today: '}

def get_results():
    resp = requests.get(api)
    result = resp.json()
    if result.get('message'):
        return None
    return result


dt = get_results()
data = [f'{d}{dt.get(f)}' for f, d in FIELDS.items()]

print(', '.join(data))