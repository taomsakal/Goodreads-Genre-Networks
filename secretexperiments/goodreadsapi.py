from goodreads import client
from bs4 import BeautifulSoup
import urllib
import time

# Key and Secret Key for accessing the api
KEY = '83miVYXm5ohZqeANTj0hLw'
SECRET = 'x5gbome6DgF2fZfiVHuQrfxndTzFQ4cMBM9EdufS1A'

goodreads = client.GoodreadsClient(KEY, SECRET)

user = goodreads.user(64962100)
print(user.name)

# https://www.goodreads.com/review/list/2?per_page=100
# https://www.goodreads.com/review/list/2?page=2&per_page=100


#
# html = urllib.request.urlopen('https://www.goodreads.com/review/list/234222?shelf=read').read()
# soup = BeautifulSoup(html, 'lxml')
#
#
# books = soup.find_all("tr", class_="bookalike review")  # Gives list of books with info
# #print(books[0])
#
# a = books[0].find_all("td", class_="field title")
# print(a)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field rating")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field author")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field isbn")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field isbn13")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field asin")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field num_pages")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field avg_rating")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field num_ratings")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field date_pub")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field date_pub_edition")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field review")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field recommender")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field notes")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field comments")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field votes")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field read_count")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field date_added")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field date_purchased")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field owned")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field purchase_location")
# print(b)
#
# print("----------")
#
# b = books[0].find_all("td", class_="field condition")
# print(b)
#
# print("----------")
#
# b = books[0].find("td", class_="field format")
#
# print(b.text)
#
#
#
#
#
