from bs4 import BeautifulSoup
import requests

from nwcrawler.config import config


def get_html_content(url):
    response = requests.get(url)
    html_content = response.text
    return html_content


def get_number_of_pages(base_url):
    html_content = get_html_content(base_url)
    soup = BeautifulSoup(html_content, "html.parser")

    def get_number(x):
        try:
            return int(x.text.replace("Página", ""))
        except:
            return None

    pag_elements = soup.findAll("nav", attrs={"class":"elementor-pagination", "aria-label":"Paginação"})
    return max([get_number(x) for x in pag_elements[0].findAll("a", class_="page-numbers") if get_number(x)])


def get_articles_within_page(page):
    def has_articles(x):
        return (
            len(
                [
                    y
                    for y in x.findAll(
                        "h2", class_="elementor-heading-title elementor-size-default"
                    )
                    if "Artigos" in y.text
                ]
            )
            > 0
        )

    url = f"{config.NW_URL}/page/{page}"
    html_content = get_html_content(url)
    soup = BeautifulSoup(html_content, "html.parser")

    results = [
        x
        for x in soup.findAll("section", class_="elementor-top-section")
        if has_articles(x)
    ]

    assert len(results) == 1, "More than one article section was found"
    articles = results[0].findAll("article")
    return articles
