from typing import Optional

from tqdm import tqdm
import typer
from loguru import logger

from nwcrawler.config import config
from nwcrawler.scraping.crawler import get_articles_within_page, get_number_of_pages
from nwcrawler.database.connection import DatabaseConnection
from nwcrawler.database.repositories import ArticleRepository
from nwcrawler.scraping.parsing import get_article_information, process_article

app = typer.Typer()
articles_app = typer.Typer()
pages_app = typer.Typer()
app.add_typer(articles_app, name="articles")
app.add_typer(pages_app, name="pages")


@articles_app.command("scrape")
def scrape(
    last_page: Optional[int] = typer.Option(
        None,
        "--last",
        "-l",
        help="Last page to scrape",
    )
):
    
    logger.debug(f"Running in '{config.ENV}' environment.")
    
    database_filepath = f"databases/{config.ENV}.db"
    db_conn = DatabaseConnection(database_filepath)

    logger.debug(f"Loaded database '{database_filepath}'.")

    article_repo = ArticleRepository(db_conn)

    max_pages = get_number_of_pages(config.NW_URL)
    logger.info(f"It was found {max_pages} article pages in '{config.NW_URL}'")
    
    if not last_page:
        last_page = max_pages

    logger.info(f"Scraping pages from 1 to {last_page}.")

    for page in range(1, last_page + 1):
        articles = get_articles_within_page(page)
        for article in tqdm(articles, total=len(articles), desc=f"Page {page}"):
            process_article(article_repo, article, overwrite=True)


@articles_app.command("show")
def show():
    database_filepath = f"databases/{config.ENV}.db"
    db_conn = DatabaseConnection(database_filepath)
    article_repo = ArticleRepository(db_conn)
    articles = article_repo.get_all()
    print(articles)


if __name__ == "__main__":
    app()
