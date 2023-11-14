from bs4 import BeautifulSoup
import requests
import datetime
from timeit import default_timer as timer
import sys
import pandas as pd
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
    print(f"Getting temperature min and max for {inputdate.strftime('%Y-%m-%d')}")

    # Args
    day = inputdate.day
    # month number is 0 indexed, apparently
    month = inputdate.month - 1
    year = inputdate.year
    url = f"https://www.meteociel.fr/temps-reel/obs_villes.php?code2=59512001&jour2={day}&mois2={month}&annee2={year}&affint=1"

    print(f"GET {url} ...")

    start = timer()
    r = requests.get(url)
    end = timer()
    duration = end - start

    print(f" ... getting URL took {duration}s of time")

    print("Parsing HTML result ...")

    start = timer()

    # Apparently this website is not using UTF encoding for some reason
    # But requests doesn't seem to care so all is well
    soup = BeautifulSoup(r.text, 'html.parser')

    # select all td tags in the relevant summary table
    tds = soup.select(".Style1 table[bgcolor='#FFFF99'] > tr:nth-child(2) td")

    # print(f"table: \n{tds}\n")

    # Flatten the list of contents
    tds_contents = [value for td in tds for value in td.contents]
    # print(tds_contents)

    end = timer()
    duration = end - start
    print(f" ... parsing HTML result took {duration}s of time")

    temps = {"date": inputdate,"min": float(tds_contents[1].replace(" °C", "")), "max": float(tds_contents[0].replace(" °C", ""))}
    return temps

def get_day_duration(inputdate):
    times = get_times(inputdate, LON, LAT)
    return (times["sunset"] - times["sunrise"]).total_seconds()

def main():
    target_year = sys.argv[1]
    # dates = [
    #     datetime.datetime.fromisoformat("2022-01-01"),
    #     datetime.datetime.fromisoformat("2022-01-02"),
    #     datetime.datetime.fromisoformat("2022-01-03"),
    #     datetime.datetime.fromisoformat("2022-01-04"),
    #     datetime.datetime.fromisoformat("2022-01-05"),
    #     datetime.datetime.fromisoformat("2022-01-06"),
    #     datetime.datetime.fromisoformat("2022-01-07"),
    #     datetime.datetime.fromisoformat("2022-01-08"),
    # ]
    dates = get_year_date_range(int(target_year))
    temps = []

    for date in dates:
        day_duration = get_day_duration(date)
        night_duration = TOTAL_DAY_DURATION - day_duration
        day_temps = get_min_max_temp_for_date(date)
        temps.append({**day_temps, "night_duration": night_duration, "day_duration": day_duration})

    df = pd.DataFrame(temps).set_index("date")
    df.to_csv(f"{target_year}_data.csv")

if __name__=="__main__": 
    main()
