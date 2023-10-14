import requests
from bs4 import BeautifulSoup
import pandas as pd


reviewlist = []
id_counter = 0

def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup):
    global id_counter
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'id': id_counter,
            'product': soup.title.text.replace('Amazon.in:Customer reviews:', '').strip(), #'product': soup.title.text.replace('Amazon.in:Customer reviews:', '').strip(),
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'username': item.find('span', {'class': 'a-profile-name'}).text.strip(),
            'rating':  int(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
            id_counter += 1
    except:
        pass

for x in range(1,999):
    soup = get_soup(f'https://www.amazon.in/HP-Micro-Edge-Anti-Glare-15s-fq5111TU/product-reviews/B0B6F5V23N/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

df = pd.DataFrame(reviewlist)
df.to_excel('Reviews.xlsx', index=False)
print('Finshed.')
