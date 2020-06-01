# 
# Calculating invoices for customer billing
# Background
# 
# In the past, we provided some raw billing data in JSON format to the finance team, which they used to manually generate monthly invoices for our customers. Recently, they’ve asked us to create some automation to make this process less error-prone.
# Instructions
# 
# Your goal is to implement the bill_for function to calculate the total monthly bill for a customer.
# 
# Customers are billed based on their subscription tier for the month. We charge them a prorated amount for each user who was active during that month.
# 
# You talked with the other engineers on the team and decided that the following algorithm would work:
# 
#     Calculate a daily rate for the active subscription tier
#     For each day of the month, identify which users were active that day
#     Multiply the number of active users for the day by the daily rate to calculate the total for the day
#     Return the running total for the month at the end, rounded to 2 decimal places
# 
# Parameters
# 
# This billing function accepts the following parameters:
# 
# month
# Always present. Has the following structure:
# 
# "2019-01"   # January 2019 in YYYY-MM format
# 
# active_subscription
# May be None. If present, has the following structure:
# 
# {
#   'id': 1,
#   'customer_id': 1,
#   'monthly_price_in_dollars': 4  # price per active user per month
# }
# 
# users
# May be empty, but not None. Has the following structure:
# 
# [
#   {
#     'id': 1,
#     'name': 'Employee #1',
#     'customer_id': 1,
# 
#     # when this user started
#     'activated_on': datetime.date(2018, 11, 4),
# 
#     # last day to bill for user
#     # should bill up to and including this date
#     # since user had some access on this date
#     'deactivated_on': datetime.date(2019, 1, 10)
#   },
#   {
#     'id': 2,
#     'name': 'Employee #2',
#     'customer_id': 1,
# 
#     # when this user started
#     'activated_on': datetime.date(2018, 12, 4),
# 
#     # hasn't been deactivated yet
#     'deactivated_on': None
#   }
# ]
# 
# Return value
# 
# This function should return the total monthly bill for the customer, rounded to 2 decimal places.
# 
# If there are no users or the subscription is not present, the function should return 0 since the customer does not owe anything for that month.
# Calculation Examples
# 
# Here is an example of calculating the amount to bill each customer using the algorithm described above. This example is captured by the "works when a user is activated during the month" test.
#     
# Month   2019-01
# Subscription tier   $4 / month
# User activations    2018-11-04
# 2018-12-04
# 2019-01-10 (new this month)
# User deactivations  None
# 
# Daily rate is $4.00 / 31 days => $0.129032258 / day
# 
# 2019-01-01  2 active users * $0.129032258 = $0.258064516  (subtotal: $0.258064516)
# 2019-01-02  2 active users * $0.129032258 = $0.258064516  (subtotal: $0.516129032)
# ...
# 2019-01-09  2 active users * $0.129032258 = $0.258064516  (subtotal: $2.322580645)
# 2019-01-10  3 active users * $0.129032258 = $0.387096774  (subtotal: $2.709677419)
# 2019-01-11  3 active users * $0.129032258 = $0.387096774  (subtotal: $4.387096772)
# ...
# 2019-01-30  3 active users * $0.129032258 = $0.387096774  (subtotal: $10.451612903)
# 2019-01-31  3 active users * $0.129032258 = $0.387096774  (subtotal: $10.838709677)
# 
# Total = $10.84 (round subtotal to nearest cent)
# 
# Testing
# 
# The automated tests we provide only cover a few key cases, so you should plan to add some of your own tests or modify the existing ones to ensure that your solution handles any edge cases. You should be able to follow the existing patterns for naming and constructing tests to add your own.
# Notes / Edge cases
# 
#     It’s more important for the return value to be correct than it is for the algorithm to be highly optimized.
#     You can store intermediate results as any kind of decimal type (e.g. float, double). You do not need to round values until the last step.
#     You should not change function names or return types of the provided functions since our test cases depend on those not changing.
# 
# Time guidance
# 
# Aim to take between 25-45 minutes for this challenge. Set a timer now for 45 minutes to gauge the time you have spent on this challenge.
# 
# If you have spent 45 or more minutes:
# 
#     Stop working
#     Document where you are at in the "Your Notes" section in the upper right corner
#     Go on to the next challenge. It is independent from any solution you got on this challenge.
#     You can return to any incomplete challenges if you have time left over at the end.

# Nuertey Odzeyem Solution:
import datetime
import calendar
from datetime import date

def bill_for(month, active_subscription, users):
    # your code here!
    total_monthly_bill = 0
    if active_subscription is None:
      total_monthly_bill = 0
    elif not users:
      total_monthly_bill = 0
    else:
      month = datetime.datetime.strptime(month, '%Y-%m')
      number_of_days = (last_day_of_month(month.date()) - first_day_of_month(month.date())).days + 1
      print(number_of_days)
      print()
      daily_rate = active_subscription['monthly_price_in_dollars']/number_of_days
      print(daily_rate)
      print()
      for user in users:
        if user['deactivated_on'] is None:
          print(user['activated_on'])
          print(user['deactivated_on'])
          user_days = (last_day_of_month(month.date()) - user['activated_on']).days + 1
          
          user_monthly_bill = user_days*daily_rate
          print(user_monthly_bill)
          print()
          total_monthly_bill = total_monthly_bill + user_monthly_bill
        else:
          print(user['activated_on'])
          print(user['deactivated_on'])
          user_days = (user['deactivated_on'] - user['activated_on']).days + 1
          
          user_monthly_bill = user_days*daily_rate
          print(user_monthly_bill)
          print()
          total_monthly_bill = total_monthly_bill + user_monthly_bill
          
    total_monthly_bill = str(round(total_monthly_bill, 2))
    return total_monthly_bill
    pass

####################
# Helper functions #
####################

def first_day_of_month(date):
    """
    Takes a datetime.date object and returns a datetime.date object
    which is the first day of that month. For example:
    
    >>> first_day_of_month(datetime.date(2019, 2, 7))  # Feb 7
    datetime.date(2019, 2, 1)                          # Feb 1
    
    Input type: datetime.date
    Output type: datetime.date
    """
    return date.replace(day=1)

def last_day_of_month(date):
    """
    Takes a datetime.date object and returns a datetime.date object
    which is the last day of that month. For example:
    
    >>> last_day_of_month(datetime.date(2019, 2, 7))  # Feb  7
    datetime.date(2019, 2, 28)                        # Feb 28
    
    Input type: datetime.date
    Output type: datetime.date
    """
    last_day = calendar.monthrange(date.year, date.month)[1]
    return datetime.date(date.year, date.month, last_day)

def next_day(date):
    """
    Takes a datetime.date object and returns a datetime.date object
    which is the next day. For example:
    
    >>> next_day(datetime.date(2019, 2, 7))   # Feb 7
    datetime.date(2019, 2, 8)                 # Feb 8

    >>> next_day(datetime.date(2019, 2, 28))  # Feb 28
    datetime.date(2019, 3, 1)                 # Mar  1
    
    Input type: datetime.date
    Output type: datetime.date
    """
    return date + datetime.timedelta(days=1)

# ==========================================
test_month = "2019-01"

test_active_subscription = {
      'id': 1,
      'customer_id': 1,
      'monthly_price_in_dollars': 4  # price per active user per month
    }

test_users = [
  {
    'id': 1,
    'name': 'Employee #1',
    'customer_id': 1,

    # when this user started
    'activated_on': datetime.date(2018, 11, 4),

    # last day to bill for user
    # should bill up to and including this date
    # since user had some access on this date
    'deactivated_on': datetime.date(2019, 1, 10)
  },
  {
    'id': 2,
    'name': 'Employee #2',
    'customer_id': 1,

    # when this user started
    'activated_on': datetime.date(2018, 12, 4),

    # hasn't been deactivated yet
    'deactivated_on': None
  }
]

print(test_month)
print()
print(test_active_subscription)
print()
print(test_users)

customer_total_billing = bill_for(test_month, test_active_subscription, test_users)

print()
print(customer_total_billing)
print()
