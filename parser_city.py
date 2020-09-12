import urllib.request
import random
from bs4 import BeautifulSoup

base_url = 'https://ru.wikinews.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
list_of_cities = []


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html, bot_letter):
    data = BeautifulSoup(html, 'html.parser')

    for group in data.find_all('div', class_='mw-category-group'):
        letter = group.find('h3')
        if letter.text == bot_letter:
            
            llist = group.find_all('li')
            random.shuffle(llist)
            for city in llist:
                
                city = city.find('a')
                city_text = city.text
                
                print(city_text)
                
                if city_text:
                    is_this_city_new = True

                    city_result = city_text.split(" (")
                    city_result_name = city_result[0]

                    for i in list_of_cities:
                        if i == city_result_name.lower():
                            is_this_city_new = False
                            break

                    if is_this_city_new:        
                    
                        list_of_cities.append(city_result_name.lower())

                        print(list_of_cities)               
                        return city_result_name
                    else:
                        city = city.find_next_sibling('a')
                        is_this_city_new = True
                        continue
  
    nextpage = ''
    for page in data.find('div', class_='mw-category-generated').find_all('a'):
    	if page.text == "Следующая страница":
    		nextpage = page.get('href')
    		break

    print(nextpage)
    if nextpage:
        return parse(get_html('https://ru.wikinews.org' + nextpage), bot_letter)


def main(bot_letter):
	return parse(get_html(base_url), bot_letter)
