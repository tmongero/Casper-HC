import requests
from pprint import pprint
import json

# Hipchat room parameters for 'tj test room'.
room_token = 'OGSxQqAg1kwLQfTQlMf70g8NcwxFPKgNrwH075w4'
room_id = '4349115'
notify_room_url = f'https://jamf.hipchat.com/v2/room/{room_id}/notification?auth_token={room_token}'

# temporarily disabled.
# # dev-casperHC integration token. Using for testing simple REST calls.
# auth_token = 'cAUrQ5vc0rGqRyQYjsXRv0nN7Eep7nfVsWGlJOGB'
# room_url = f'{url}/room/4349115'
# room_url = f'https://jamf.hipchat.com/v2/room/4349115/notification?auth_token={auth_token}'

s = requests.Session()
s.headers.update(
    {
        'Authorization': f'Bearer {room_token}',
        'Accept': 'application/json',
        # 'Content-Type': 'application/json',
    }
)

payload = {
    "color":"purple",
    "message":"First steps in building integration",
    "notify":False,
    "message_format":"text"
}

pprint(payload)

r = s.post(url=notify_room_url, data=payload)
print(r.ok)
print(r.reason)
print(r.content)
# pprint(r.json())