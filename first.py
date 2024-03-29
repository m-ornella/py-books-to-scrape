import requests
from bs4 import BeautifulSoup
import csv


# get single book details
def get_book(url):
    page = requests.get(url)
    product_description = ""

    soup = BeautifulSoup(page.text, "html.parser")

    # retrieves single book details using selectors
    title = soup.select_one("h1").text
    universal_product_code = soup.select_one("table tr:first-child td").text
    price_including_tax = soup.select_one("table tr:nth-child(3) td").text.replace(
        "Â£", ""
    )
    price_excluding_tax = soup.select_one("table tr:nth-child(4) td").text.replace(
        "Â£", ""
    )
    number_available = soup.select_one("table tr:nth-child(6) td").text
    if soup.select_one(".product_page > p") is not None:
        product_description = soup.select_one(".product_page > p").text

    category = soup.select_one(".breadcrumb li:nth-child(3) a").text
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    image_url = [img["src"] for img in soup.select(".carousel-inner img[src]")][0]

    # dictionary
    book_info = {
        "title": title,
        "universal_product_code": universal_product_code,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url[5:],
    }

    # csv file
    with open("book.csv", "w") as f:
        for key, value in book_info.items():
            f.write(f"{key},{value}\n")

    return book_info


# replace url with any single book url
# book_data = get_book(
#     "https://books.toscrape.com/catalogue/the-metamorphosis_409/index.html"
# )
# print(book_data)
