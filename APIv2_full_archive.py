### Twitter API v2 Academic Track Full Archive Search###


import requests
import pandas as pd
import json
import time

def search_endpoint_connect(bearer_token, query, st, et, next_token):
    
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    query_params = {
                    'query': query,
                    'start_time': st,
                    'end_time': et,
                    'max_results': 500,
                    'tweet.fields': 'id,text,author_id,created_at,geo,lang,public_metrics,in_reply_to_user_id',         
                   }
    
    if (next_token is not None):
        url = "https://api.twitter.com/2/tweets/search/all?next_token={}".format(next_token)
    else:
        url = "https://api.twitter.com/2/tweets/search/all"
    
    response = requests.request("GET", url, params=query_params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    
    return response.json()

def main(bearer_token, n, fn, sq, st, et):
    
    count = 0
    flag = True
    first = True


    while flag:
        

        if count >= n and n!=0:
            break
        if not first:
            json_response = search_endpoint_connect(bearer_token, sq, st, et, next_token)
        else:
            json_response = search_endpoint_connect(bearer_token, sq, st, et, next_token=None)
        
        result_count = json_response['meta']['result_count']
        if 'next_token' in json_response['meta']:
            next_token = json_response['meta']['next_token']
        
        if result_count is not None and result_count > 0:
            
            df = pd.json_normalize(json_response['data'])
            df = df.reindex(columns=['id', 'author_id', 'created_at', 'text', 'lang', 'public_metrics.retweet_count',
                                     'public_metrics.reply_count', 'public_metrics.like_count', 'public_metrics.quote_count',
                                    'in_reply_to_user_id', 'geo.place_id', 'geo.coordinates.type', 'geo.coordinates.coordinates'])
            if not first:
                df.to_csv('%s.csv'%fn, mode='a', encoding='utf-8', index=False, header=None)
            else:
                df.to_csv('%s.csv'%fn, encoding='utf-8', index=False)

        time.sleep(3.1)
        count += result_count
        print('Tweets downloaded: '+str(count))
        if 'next_token' not in json_response['meta']:
            flag = False
        first = False


#Enter your bearer token
bearer_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

#Set number of tweets to be downloaded. Enter 0 for no limits
no_of_tweets = 20

#Specify the name of the output csv file. Do not include .csv
file_name = 'downloaded_tweets'

#Enter your search query. Refer to https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
search_query = '#your #query #here'

#Set the beginning date and time in YYYY-MM-DDTHH:MM:SSZ format
start_time = "YYYY-MM-DDTHH:MM:SSZ"

#Set the ending date and time in YYYY-MM-DDTHH:MM:SSZ format
end_time = "YYYY-MM-DDTHH:MM:SSZ"

main(bearer_token, no_of_tweets, file_name, search_query, start_time, end_time)