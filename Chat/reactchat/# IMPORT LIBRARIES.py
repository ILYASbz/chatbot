# IMPORT LIBRARIES
from bs4 import BeautifulSoup
import requests

# REQUEST WEBPAGE AND STORE IT AS A VARIABLE
page_to_scrape = requests.get("http://www.meteomaroc.com/meteo/casablanca")
# USE BEAUTIFULSOUP TO PARSE THE HTML AND STORE IT AS A VARIABLE
soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
# FIND ALL THE ITEMS IN THE PAGE WITH A CLASS ATTRIBUTE OF 'TEXT'
# AND STORE THE LIST AS A VARIABLE
dates = soup.findAll('label', attrs={'class': 'time-small'})
temperature = soup.findAll('label', attrs={'class': 'observation_c-small'})
rainpercentage = soup.findAll('li', attrs={'class': 'precipmm'})
rain1 = soup.findAll('li', attrs={'class': 'precipmm-0'})

# LOOP THROUGH BOTH LISTS USING THE 'ZIP' FUNCTION
# AND PRINT AND FORMAT THE RESULTS
for date, temp, ra, rai in zip(dates, temperature, rainpercentage, rain1):
    print("date"+date.text+"-température="+temp.text+"-précipitations:"+ra.text +"-"+rai.text)
