from bs4 import BeautifulSoup
import requests

filename = '20231108.html'

url = "https://www.meteociel.fr/temps-reel/obs_villes.php?code2=59512001&jour2=12&mois2=9&annee2=2023&affint=1"
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
