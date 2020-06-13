import pycountry
import pycountry

pd.set_option('display.max_rows', 100)

df = pd.DataFrame({"country_code": ['AF', 'BEL', 'AUS', 'DE', 'IND', 'US', 'GBR','XYZ'],
              "amount": [100, 200, 140, 400, 225, 125, 600,0]})

print(df)
print()

list_alpha_2 = [i.alpha_2 for i in list(pycountry.countries)]
list_alpha_3 = [i.alpha_3 for i in list(pycountry.countries)]   

print(list_alpha_2)
print()
print(list_alpha_3)
print() 

def country_flag(df):
    if (len(df['country_code'])==2 and df['country_code'] in list_alpha_2):
        return pycountry.countries.get(alpha_2=df['country_code']).name
    elif (len(df['country_code'])==3 and df['country_code'] in list_alpha_3):
        return pycountry.countries.get(alpha_3=df['country_code']).name
    else:
        return 'Invalid Code'

df['country_name'] = df.apply(country_flag, axis = 1)
print(df)
print()

#    amount country_code    country_name
# 0     100           AF     Afghanistan
# 1     200          BEL         Belgium
# 2     140          AUS       Australia
# 3     400           DE         Germany
# 4     225          IND           India
# 5     125           US   United States
# 6     600          GBR  United Kingdom
# 7       0          XYZ    Invalid Code
