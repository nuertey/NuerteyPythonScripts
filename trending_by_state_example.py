from time import sleep
from pytrends.request import TrendReq
pytrend = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)

Make a loop that downloads data for each state each
state_list1=['NG-AB', 'NG-AD', 'NG-AK', 'NG-AN', 'NG-BA', 'NG-BE']

state_data = pd.DataFrame(columns=['date','isPartial', 'state'])
for state in state_list1:
    pytrend.build_payload(kw_list=['hausa'], cat=0, timeframe= '2014-01-01 2014-06-01', geo=state)
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df.reset_index(inplace=True)
    interest_over_time_df['state']=state
    # This is inefficient. Should use list and then concatenate lists
    # into a bigger list the convert to Pandas dataframe at end.
    state_data=pd.concat([state_data, interest_over_time_df], ignore_index=True, sort=False)

state_data.to_csv('out/hausa_list1_y14_1.csv')
state_data
