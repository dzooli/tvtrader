from sys import argv
from datetime import datetime
import random
import requests


post_url = 'http://localhost:8089/carbon-alert'
valid_dirs = ['BUY', 'SELL']

data = {
    'stratId': 1,
    'stratName': 'LWMA',
    'interval': 15,
    'direction': 'SELL',
    "symbol": "FXCM:GBPUSD",
    "timestamp": '<TIMEHERE>'
}

argno = len(argv)
if argno == 2 and argv[1] == '--help':
    prgname = argv[0].split('/')[-1]
    print(f"""
    Test data generator for the tvAlert application.

    Usage:
        {prgname} --help :     This help message

        {prgname} [STRATNAME] [SYMBOLNAME] :
                    STRATNAME:      The name of the strategy
                    SYMBOLNAME:     The symbol's name
    """)
    exit(0)

if argno > 1:
    data['stratName'] = argv[1]
if argno > 2:
    data['symbol'] = argv[2]

random.shuffle(valid_dirs)
data['direction'] = valid_dirs[0]
data['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
print(data)
response = requests.post(post_url, json=data, verify=False)
print(response.json())
