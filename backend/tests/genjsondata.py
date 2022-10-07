from sys import argv
import datetime
import random
import requests


post_url = 'http://localhost:8089/carbon-alert'
valid_dirs = ['BUY', 'SELL']
time_before = None

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

        {prgname} <STRATNAME> <SYMBOLNAME> <TIME>
                    Generates alerts with outdated timestamp
    """)
    exit(0)

if argno > 1:
    data['stratName'] = argv[1]
if argno > 2:
    data['symbol'] = argv[2]
    if argno == 4 and argv[3] is not None:
        try:
            time_before = int(argv[3])
        except ValueError:
            print("Time value must be an integer!")
            exit(1)

currtime = datetime.datetime.utcnow()
sendtime = currtime
if time_before is not None:
    print(f"Required time delta is: {time_before}")
    sendtime = currtime - datetime.timedelta(minutes=time_before)
random.shuffle(valid_dirs)
data['direction'] = valid_dirs[0]
data['timestamp'] = sendtime.strftime('%Y-%m-%dT%H:%M:%SZ')
print(sendtime)
print(data)
try:
    response = requests.post(post_url, json=data, verify=True, timeout=3)
except ValueError:
    print("Connection error")
    exit(2)
print(response.json())
