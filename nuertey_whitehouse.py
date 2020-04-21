#***********************************************************************
# @file
#
# A small Python teaching script for querying White House petitions
# via the newly-available API.
#
# @note 
#
# @warning  None
#
#  Created: Dawn, April 21, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/ 
import requests
import json
import pandas as pd

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_colwidth', -1)

# UNIX Timestamp - Epoch Converter:
# ---------------------------------
# https://www.unixtimestamp.com/

URL = "https://api.whitehouse.gov/v1/petitions.json?limit=40&offset=0&createdBefore=1587455758&sortBy=date_reached_public&sortOrder=desc"

r = requests.get(URL)

if r.ok:
    print("HTTP Response Status Code:-> ", r.status_code)
    print("HTTP Response Content Type:-> ", r.headers['content-type'])
    print("HTTP Response Encoding:-> ", r.encoding)
    print()

    text_data = r.text
    json_dict = json.loads(text_data)

    data = pd.DataFrame.from_dict(json_dict["results"])
    #print(data)
    #print()

    sorted_data = data.sort_values(by=['signatureCount'], ascending=False)
    #print(sorted_data)
    #print()

    of_interest = pd.DataFrame(index=sorted_data.index)
    of_interest['signatureCount'] = sorted_data['signatureCount']
    of_interest['title'] = sorted_data['title']
    print(of_interest)
    print()

    data.to_excel("whitehouse_output.xlsx") 
else:
    print('Error! Issue with the URL, HTTP Request, and/or the HTTP Response')
