from bs4 import BeautifulSoup
import requests
import datetime
import sys
from dateutil import relativedelta as rdt

def get_year_date_range(year):
    startdate = datetime.datetime.fromisoformat(f"{year}-01-01")
    enddate = startdate + rdt.relativedelta(years=+1)
    return (startdate + datetime.timedelta(n) for n in range(0, (enddate-startdate).days))

def get_min_max_temp_for_date(inputdate):

    day = inputdate.day
    # month number is 0 indexed, apparently
    month = inputdate.month - 1
    year = inputdate.year
    url = f"https://www.meteociel.fr/temps-reel/obs_villes.php?code2=59512001&jour2={day}&mois2={month}&annee2={year}&affint=1"
    r = requests.get(url)

    # Apparently this website is not using UTF encoding for some reason
    # But requests doesn't seem to care so all is well
    soup = BeautifulSoup(r.text, 'html.parser')

    # select all td tags in the relevant summary table
    tds = soup.select(".Style1 table[bgcolor='#FFFF99'] > tr:nth-child(2) td")

    # print(f"table: \n{tds}\n")

    # Flatten the list of contents
    tds_contents = [value for td in tds for value in td.contents]
    # print(tds_contents)

    temps = {"min": tds_contents[1], "max": tds_contents[0]}
    return temps

def main():
    dates = get_year_date_range(2023)
    date = next(dates)
    temps = get_min_max_temp_for_date(date)
    print(temps)

    print("I would also have fetched min max temps for dates:")
    for date in dates:
        print(date.strftime("%Y-%m-%d"))

if __name__=="__main__": 
    main()
