import requests
import pandas as pd

content = requests.get('https://codeforces.com/api/contest.list?gym=false')

df = pd.DataFrame(content.json()['result'])
df.drop(columns=['phase','frozen','durationSeconds','relativeTimeSeconds'],inplace=True)
df.to_csv('contests.csv',encoding='utf-8', index=False)