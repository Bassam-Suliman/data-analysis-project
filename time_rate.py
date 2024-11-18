import requests
import pandas as pd
import numpy as np


Left = int(input('Left interval: '))
Right = int(input('Right interval: '))
contestID = int(input('Contest ID: '))

if Left > Right:
    print('Don\'t do dis')
    input('Type anything to exit!')
    exit()
    

page = requests.get(f'https://codeforces.com/api/contest.standings?contestId={contestID}&from=1&count=50000&showUnofficial=false')
Start = page.json()['result']['contest']['startTimeSeconds']

changes = requests.get(f'https://codeforces.com/api/contest.ratingChanges?contestId={contestID}')
changes = pd.DataFrame(changes.json()['result'],columns=['contestId','contestName','handle','rank','ratingUpdateTimeSeconds','oldRating','newRating'])
changes.drop(columns=['contestId','contestName','ratingUpdateTimeSeconds'],inplace=True)
changes.set_index('handle',inplace=True)


### Preparing the map for each problem
mp = {}
indices = []
for problem in page.json()['result']['problems']:
    mp[problem['index']] = []
    indices.append(problem['index'])


### Main area
for row in page.json()['result']['rows']:
    try :
        handle = row['party']['members'][0]['handle']
        cur_rate = changes.loc[handle]['oldRating']
        
        if cur_rate > Right or cur_rate < Left:
            continue

        probs = pd.DataFrame(data=row['problemResults'],columns=['points','rejectedAttemptCount','type','bestSubmissionTimeSeconds'])
        probs = pd.concat([probs,pd.Series(indices,name='index')],axis=1)
        probs.set_index('index',inplace=True)
        probs = probs[probs.points > 0]
        probs.drop(columns=['points','rejectedAttemptCount','type'],inplace=True)
        last = 0
        for ind in probs.sort_values(by='bestSubmissionTimeSeconds').index:
            cur = probs.loc[ind]['bestSubmissionTimeSeconds']
            mp[ind].append((cur-last)/60)
            last = cur
        ###print(handle,cur_rate)
    except:
        pass

for key in mp.keys():
    print('Problem',key)
    try:
        se = pd.Series(mp[key]).describe().astype(dtype='int')
        print(f'Fastest user to solve took {se['min']} minutes.')
        print(f'25% of users solved it under {se['25%']+1} minutes.')
        print(f'50% of users solved it under {se['50%']+1} minutes.')
        print(f'75% of users solved it under {se['75%']+1} minutes.')
        print(f'Slowest user to solve took {se['max']} minutes.')
    except:
        print('No one solved this problem!')
    print()
    

input('Type anything to exit!')

### This script tells how much time people have taken to solve some problem
### for example in contests 2026 and users with rating between 1900 and 2100
