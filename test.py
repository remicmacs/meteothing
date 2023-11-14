from bs4 import BeautifulSoup
import requests
import datetime
import sys
from dateutil import relativedelta as rdt
from suncalc import get_position, get_times

LON = 3.167050
LAT = 50.683330
TOTAL_DAY_DURATION = datetime.timedelta(days=1).total_seconds()

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

    temps = {"date": inputdate,"min": tds_contents[1], "max": tds_contents[0]}
    return temps

def get_day_duration(inputdate):
    times = get_times(inputdate, LON, LAT)
    return (times["sunset"] - times["sunrise"]).total_seconds()

def main():
    target_year = sys.argv[1]
    dates = [
        datetime.datetime.fromisoformat("2022-01-01"),
        datetime.datetime.fromisoformat("2022-01-02"),
        # datetime.datetime.fromisoformat("2022-01-03"),
        # datetime.datetime.fromisoformat("2022-01-04"),
        # datetime.datetime.fromisoformat("2022-01-05"),
        # datetime.datetime.fromisoformat("2022-01-06"),
        # datetime.datetime.fromisoformat("2022-01-07"),
        # datetime.datetime.fromisoformat("2022-01-08"),
    ]
    # dates = get_year_date_range(int(target_year))
    temps = [ {**get_min_max_temp_for_date(date), "day_duration": get_day_duration(date)} for date in dates]

    print(temps)

    # date = next(dates)
    # temps = get_min_max_temp_for_date(date)
    # print(temps)
    #
    # print("I would also have fetched min max temps for dates:")
    # for date in dates:
    #     print(date.strftime("%Y-%m-%d"))

if __name__=="__main__": 
    main()
