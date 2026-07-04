# Zironlink -- public redacted build. Full source in the private repo.

import requests
import json
LAVALINK_HOST = 'http://localhost:2333'
LAVALINK_PASSWORD = 'youshallnotpass'
headers = {'Authorization': LAVALINK_PASSWORD, 'Accept': 'application/json'}
try:
    response = requests.get(f'{LAVALINK_HOST}/v4/info', headers=headers, timeout=10)
    print(f'Status Code: {response.status_code}')
    if response.ok:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print(response.text)
except requests.exceptions.ConnectionError:
    print('Could not connect to Lavalink. Is it running on port 2333?')
except requests.exceptions.Timeout:
    print('Request timed out.')
except Exception as e:
    print(f'Error: {e}')
