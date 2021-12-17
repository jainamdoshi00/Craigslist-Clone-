import requests
from requests.compat import quote_plus #whenever we search anything like python space tutor it will automatically put + sign between python and tutor it will look like url
from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup
BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')
def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)  #it will give search content to database
    #print(quote_plus(search)) #if python space tutor then we will insert + sign between python and tutor
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search)) #it will concatenate base craiglist url with quoteplus
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data,features='html.parser')
    post_listings = soup.find_all('li',{'class':'result-row'}) #it will give all anchor links with class=result-title
    post_title = post_listings[0].find('a',{'class':'result-title'}).text
    post_url = post_listings[0].find('a').get('href')
    #post_price = post_listings[0].find('span',{'class':'result-price'}).text
    #d = soup.find_all('span',{'class':'result-price'})
    final_postings=[]
    for post in post_listings:
        post_title = post.find('a',{'class':'result-title'}).text
        post_url = post.find('a').get('href')
        if post.find('span',{'class':'result-price'}):
            post_price = post.find('span',{'class': 'result-price'}).text
        else:
            post_price = 'Not Mentioned'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1] #long story soup se image nahi aa raha tha
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_postings.append((post_title,post_url,post_price,post_image_url))
    #print(final_postings)
    #print(d[0].text)
    #print(post_title)
    #print(post_url)
    #print(post_price)
    #print(response)
    #print(final_url)

    #print(search)
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    print(search)
    return render(request, 'my_apps/new_search.html', stuff_for_frontend)
