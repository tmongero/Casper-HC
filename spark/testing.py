import requests

s = requests.Session()
s.headers.update(
    {
        'Accept': 'application/json',
        'Authorization': 'Bearer NTBmMjE4NTItNWViOC00MDhmLWFkZmUtNTk5YWFhNTFkMGVjNDZmOTQ1ODQtY2Ux'
    }
)

url = 'https://api.ciscospark.com/v1/people'
all_users = list()


def caller(_url=None):
    r = s.get(_url)
    print(r.ok)
    print(len(r.json()['items']))
    all_users.extend(r.json()['items'])
    print(len(all_users))
    if r.links:
        print('found links: ', r.links)
        caller(_url=r.links['next']['url'])

def post_to_spark():
    emily = [x for x in all_users if x['displayName'] == 'Emily Houchins'][0]

    payload = {'toPersonId': emily['id'], 'text': 'This message was sent using the Cisco Spark API! :D'}

    r = s.post(url.replace('people', 'messages'), data=payload)
    print(r.ok)

def main():

    caller(_url=url)
    print(len(all_users))
    post_to_spark()


if __name__ == "__main__":
    main()
