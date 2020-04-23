#***********************************************************************
# @file
#
# Small python script illustrating how to generate scatter plots on 
# Mapbox maps in Python. 
#
# @note Before the script dives into the work of its main purpose, it 
#       also attempts to illustrate the myriad ways of achieving bash
#       shell command execution from python.
#
# @warning  None
#
#  Created: Twilight of April 22, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import subprocess 
import plotly.express as px # Plotly Express is the easy-to-use, high-level
                            # interface to Plotly, which operates on "tidy"
                            # data and produces easy-to-style figures.

# Illustrating one way to achieve bash command execution from python:
external_bash_command = 'df'
command_arguments = '-alh'
normal = subprocess.run([external_bash_command, command_arguments],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    check=True,
    text=True)
print(normal.stdout)
print()

# Illustrating another way to achieve bash command execution from python:
correct = subprocess.run(['dig', '+noshort', 'stackoverflow.com'],
    check=True, text=True)
print(correct.stdout)
print()

# Illustrating yet another way NOT to achieve bash command execution from python:
#cmd = '''while read -r x;
#   do ping -c 3 "$x" | grep 'round-trip min/avg/max'
#   done <example_hosts.txt'''
#
## Trivial but horrible
#results = subprocess.run(
#    cmd, shell=True, universal_newlines=True, check=True)
#print(results.stdout)
#print()

# Reimplement with shell=False
with open('example_hosts.txt') as hosts:
    for host in hosts:
        host = host.rstrip('\n')  # drop newline
        ping = subprocess.run(
             ['ping', '-c', '3', host],
             text=True,
             stdout=subprocess.PIPE,
             check=True)
        for line in ping.stdout.split('\n'):
             if 'round-trip min/avg/max' in line:
                 print('{}: {}'.format(host, line))
print()

# ============================================================
# Actual purpose of this script follows:
# ============================================================

# To plot on Mapbox maps with Plotly, a Mapbox account and a public 
# Mapbox Access Token is needed. Let's just use mine:
px.set_mapbox_access_token(open(".mapbox_token").read())


data = px.data.carshare()
figure = px.scatter_mapbox(data, lat="centroid_lat", lon="centroid_lon",
    color="peak_hour", size="car_hours",
    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, 
    zoom=10)
figure.show()
