from bs4 import BeautifulSoup

filename = '20231108.html'

with open(filename, 'r', encoding='ISO-8859-1') as file:
    file_contents = file.read()

# TODO: handle if no contents
soup = BeautifulSoup(file_contents, 'html.parser')

res = soup.select(".Style1 table[bgcolor='#FFFF99']")
print(res)
