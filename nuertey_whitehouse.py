import requests
import json
import pandas as pd

pd.set_option('display.max_rows', 100)

#URL = "https://api.whitehouse.gov/v1/petitions.json?limit=20&offset=0&createdBefore=1573862400"
URL = "https://api.whitehouse.gov/v1/petitions.json?limit=20&offset=0"

# fetching the json response from the URL
r = requests.get(URL)

if r.ok:
    print("HTTP Response Status Code:-> ", r.status_code)
    print("HTTP Response Content Type:-> ", r.headers['content-type'])
    print("HTTP Response Encoding:-> ", r.encoding)
    print()

    text_data = r.text
    #print(r.text)
    json_dict = json.loads(text_data)

    # converting json dictionary to python dataframe for results object
    df = pd.DataFrame.from_dict(json_dict["results"])
    #data = pandas.DataFrame.from_dict(r.json())
    print(df)
    print()

    df.to_excel("whitehouse_output.xlsx") 
else:
    print('Error! Issue with the URL, HTTP Request, and/or the HTTP Response')
