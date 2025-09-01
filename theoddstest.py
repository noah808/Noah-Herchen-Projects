import requests
import json
API_KEY = '' # PASTE YOUR API KEY FROM https://api.the-odds-api.com/ HERE

# PASTE SPORT KEY FROM https://the-odds-api.com/sports-odds-data/sports-apis.html BELOW
SPORT = 'tennis_atp_cincinnati_open'

REGIONS = 'us' # uk | us | us2 | eu | au

# Grab spreads, totals, and moneylines
MARKETS = 'spreads,totals,h2h'

# Specify odds format
ODDS_FORMAT = 'american' # decimal | american

# Specify date format
DATE_FORMAT = 'iso' # iso | unix

# Fetch a list of events
events_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/events', params={
    'api_key': API_KEY,
})

if events_response.status_code != 200:
    print(f'Failed to get sports: status_code {events_response.status_code}, response body {events_response.text}')
    exit()

events_json = events_response.json()
if len(events_json) == 0:
    print('No events found')
    exit()

# json to fill with each game
full_json = {"games": []}

for event in events_json:
    # call api
    odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/events/{event["id"]}/odds',
                                 params={
                                     'api_key': API_KEY,
                                     'regions': REGIONS,
                                     'markets': MARKETS,
                                     'oddsFormat': ODDS_FORMAT,
                                     'dateFormat': DATE_FORMAT,
                                 })

    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
        # convert api call to dict
        odds_json = odds_response.json()
        # pretty print odds response
        full_json["games"].append(odds_json)
        print(json.dumps(odds_json, indent=2))

        # Print used and remaining credits
        print('Total credits remaining', odds_response.headers['x-requests-remaining'])
        print('Total credits used', odds_response.headers['x-requests-used'])

# write to json file for comparelines.py to read in
with open("data.json", "w") as json_file:
    json.dump(full_json, json_file, indent=4)