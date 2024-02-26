import requests
from bs4 import BeautifulSoup
import csv


# retrieving details from all books


def navigate_to_next_page(soup, category_name, category_id):
    next_button = soup.find("li", class_="next")
    if next_button and next_button.find("a"):
        next_page_url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/{next_button.find('a')['href']}"
        return next_page_url
    return None


# navigate to all category urls
def navigate_through_all_categories(url) -> list[str]:

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    base_url = "https://books.toscrape.com/"

    category_urls = soup.select(".nav-list li ul li a")

    category_links = []

    for category_url in category_urls:
        href = base_url + category_url.get("href")
        category_infos = extract_category_infos(href)
        category_links.append(category_infos)

    return category_links


# loop through all book urls in travel category
def get_books_urls_by_category(category_name, category_id) -> list[str]:
    base_url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"
    current_page_url = base_url

    book_urls = []

    while current_page_url:
        page = requests.get(current_page_url)
        soup = BeautifulSoup(page.text, "html.parser")

        for book in soup.find_all("article", class_="product_pod"):
            link = book.find("a")
            book_url = link.get("href")
            absolute_book_url = f"https://books.toscrape.com/catalogue/{book_url[9:]}"
            book_urls.append(absolute_book_url)

        # Navigate to the next page if available
        current_page_url = navigate_to_next_page(soup, category_name, category_id)

    return book_urls


# loop through all books to retrieve their details using the first function's url loop
def get_books_by_category(category_name, category_id) -> list[dict]:
    book_urls = get_books_urls_by_category(category_name, category_id)

    books = []

    for book_url in book_urls:
        book_details = get_book(book_url)
        books.append(book_details)

    return books


def extract_category_infos(url) -> list[str, int]:
    category_infos = url.split("/")[-2].split("_")

    return category_infos


# def get_all_books_details(category_name, category_id, url):
#     navigate_through_all_categories(url)

#     return all_book_details


urls = navigate_through_all_categories("https://books.toscrape.com/index.html")
print(urls)
