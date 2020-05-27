#***********************************************************************
# @file
#
# Python script that allows the user to search for flights and receive 
# flight prices for any valid destination world-wide. It also enables
# the user receive live quotes directly from ticketing agencies.
#
# @note     None
#
# @warning  None
#
#  Created: May 26, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import os
import sys
import argparse
import requests
import pandas as pd

pd.set_option('display.max_rows', 100)

url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/UK/GBP/en-GB/"

querystring = {"query":"Stockholm"}

headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "SIGN-UP-FOR-KEY"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
