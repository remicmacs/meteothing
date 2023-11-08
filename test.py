from bs4 import BeautifulSoup

filename = '20231108.html'

# Apparently this website is not using UTF encoding for some reason
with open(filename, 'r', encoding='ISO-8859-1') as file:
    file_contents = file.read()

# TODO: handle if no contents
soup = BeautifulSoup(file_contents, 'html.parser')

# select all td tags in the relevant summary table
tds = soup.select(".Style1 table[bgcolor='#FFFF99'] > tr:nth-child(2) td")

# print(f"table: \n{tds}\n")

# Flatten the list of contents
tds_contents = [value for td in tds for value in td.contents]
# print(tds_contents)

temps = {"min": tds_contents[1], "max": tds_contents[0]}
print(temps)
