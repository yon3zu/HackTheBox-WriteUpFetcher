import requests, time, os
import json
# from dotenv import load_dotenv
from pathlib import Path

# load_dotenv()

key = os.environ.get("KEY")

def reQ(url):
    r = requests.get(url,
        headers={
            "authority": "www.hackthebox.com",
            "authorization": "Bearer {}".format(key),
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://app.hackthebox.com/",
            "origin": "https://app.hackthebox.com/",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "accept-language": "en-US,en;q=0.9"
        }
    )
    return r

def downWU(url, Id, fileName):
    wuR = reQ(url)

    # Retrieve HTTP meta-data
    if wuR.status_code == 200:
        filename = wuR.headers["Content-Disposition"].split("=")[1]

        with open(fileName, 'wb') as f:
            f.write(wuR.content)
        print(Id, filename)
        return True
    elif wuR.status_code == 404:
        print(Id, wuR.status_code)
        return True
    elif wuR.status_code == 400:
        if (wuR.json() == {'message': 'Writeups are available only to VIP Subscribers.'}):
            print(Id, "VIP only")
        else:
            print(Id, wuR.status_code)
    else:
        # 429
        print(Id, wuR.status_code)
        print("sleeping for 50 sec")
        time.sleep(50)
        return False


res = reQ(
    'https://www.hackthebox.com/api/v4/machine/list/retired/paginated?sort_type=asc&per_page=100'
).json()

start_page=1
last_page = res['meta']['last_page']
total = res['meta']['total']

data_all = []

for current_page in range(start_page, last_page+1):
    res_ = reQ("{}&page={}".format(
        'https://www.hackthebox.com/api/v4/machine/list/retired/paginated?sort_type=asc&per_page=100', 
        current_page)).json()
    data = res_['data']
    data_all += data

print("count matches? {}".format(len(data_all)==total))

remains =[]
for x in data_all:
    Id = x['id']
    fileName = "files/{}_{}.pdf".format(Id, x['name'])
    if not Path(fileName).is_file():
        if not downWU(
            'https://www.hackthebox.com/api/v4/machine/writeup/{}'.format(Id),
            Id,
            fileName
        ):
            remains.append([Id, x['name']])
        time.sleep(7)
print("remaining: {}".format(remains))
