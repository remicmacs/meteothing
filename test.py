from bs4 import BeautifulSoup
import requests

filename = '20231108.html'

day = 12
# month number is 0 indexed, apparently
month = 10 - 1
year = 2023
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
print(temps)
