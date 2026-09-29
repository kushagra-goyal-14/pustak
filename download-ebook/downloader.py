from libgen_api import LibgenSearch
import requests
from bs4 import BeautifulSoup

def download(URL, file_format="pdf", author=""):

    URL, author = URL.strip(), author.strip()
    if file_format not in ("pdf", "epub"):
        raise ValueError("Choose PDF or EPUB.")
    if not URL and not author:
        raise ValueError("Enter a title or author.")

    # Read the book title fronm amazon.

    if 'amazon.in' in URL:

        raw = requests.get(URL,headers={'User-agent': 'Chrome'}, timeout=15)

        data = BeautifulSoup(raw.content, 'html5lib')

        raw_title = data.find('span', class_='a-size-extra-large').text

        title = raw_title.lstrip('\n').rstrip('\n').replace('()', '')

    # Read the book title from a flipkart.
    elif 'flipkart.com' in URL:

        raw = requests.get(URL,headers={'User-agent': 'Chrome'}, timeout=15)

        data = BeautifulSoup(raw.content, 'html5lib')

        raw_title = data.find('span', class_='B_NuCI').text

        title = ''

        for i in raw_title:

            if i != '(':

                title += i

            else:

                break

    else:

        title = URL  # Treat other input as a book title.

    library = LibgenSearch()

    filters = {"Extension": file_format}

    if title:
        if author:
            filters["Author"] = author
        results = library.search_title_filtered(title, filters, exact_match=False)
    else:
        results = library.search_author_filtered(author, filters, exact_match=False)

    if not results:
        raise ValueError("No matching ebook found.")

    item_to_download = results[0]

    download_links = library.resolve_download_links(item_to_download)

    return download_links['Cloudflare']
