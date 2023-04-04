import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.thewhiskyexchange.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.2526.106 Safari/537.36 Cent/1.6.10.21'
    }


productlinks = []
for x in range(1,3):
    r = requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}',headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')




    productlist = soup.find_all('li', class_="product-grid__item")
    for item in productlist:
        for link in item.find_all('a',href=True):
            productlinks.append(baseurl + link['href'])
# print(productlinks)

#testing with one link 
# testlink = 'https://www.thewhiskyexchange.com/p/29388/hibiki-harmony'


whisky_list = []
for link in productlinks:
    re = requests.get(link,headers=headers)
    # print(re) #checking whether response is 200 or we have been blocked
    soupe = BeautifulSoup(re.content, 'lxml')

    name = soupe.find('h1', class_="product-main__name").text.strip()

    try:
        ratings = soupe.find('p', class_='review-overview__content').text.strip()[0]
        reviews = soupe.find('p', class_='review-overview__content').text.split()[1].strip("(")
    except:
        ratings = "No rating"
        reviews = "No review"

    inStock= soupe.find('p', class_="product-action__stock-flag").text.strip()
    price = soupe.find('p',class_='product-action__price').text
    # print(name, ratings, reviews, inStock, price)
    whisky = {
        'name':name,
        'rating':ratings,
        'reviews':reviews,
        'inStock':inStock,
        'price':price
    }
    whisky_list.append(whisky)
    print("Saved! ", name)

df = pd.DataFrame(whisky_list)
df.to_csv('whisky_list.csv',header=True,index=False)
# print(df.head(10))
