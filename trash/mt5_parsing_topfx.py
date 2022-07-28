from requests_html import HTMLSession
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

symbols = ('EURUSD', 'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD')
tomorrow = str(datetime.date(datetime.today()) - timedelta(days=1))
link = 'https://swap.topfx.com.sc/en/swap/institutional-rates/2022-07-20'
print(link)

session = HTMLSession()
content = session.get(link)
content.html.render()
content = content.text

# with open('txt\src.txt', 'w') as file:
#     file.write(src)
# with open("src.html", "r") as f:
#     contents = f.read()

soup = BeautifulSoup(content, 'lxml')
soup_td = soup.find_all('td')

result_list = []
i = 0
while i < len(soup_td):
    if soup_td[i].text in symbols:
        result_list.append(soup_td[i].text)
        result_list.append(soup_td[i+3].text)
        result_list.append(soup_td[i+4].text)
    i += 1

print(result_list)

i = 0
while i < len(result_list):
    if result_list[i] in symbols:
        result_list[i+1] = str(round(float(result_list[i+1])*2, 5))
        result_list[i+2] = str(round(float(result_list[i+2])*2, 5))
    i += 1

print(result_list)
print('Кто молодец? Я молодец! Кто молодец? Я молодец! Кто молодец? Я молодец! :)))')
