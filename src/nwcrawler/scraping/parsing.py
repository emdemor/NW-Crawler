from datetime import datetime

import bs4
from loguru import logger
from bs4 import BeautifulSoup
from sqlite3 import IntegrityError
from unstructured.partition.html import partition_html

from nwcrawler.database.repositories import ArticleRepository
from nwcrawler.exceptions import DuplicateArticleError
from nwcrawler.scraping.crawler import get_html_content
from nwcrawler.utils.helpers import create_hash


def get_content(html_raw_content):
    soup = BeautifulSoup(html_raw_content, "html.parser")
    section_to_remove = soup.find("section", class_="post-newsform")
    if section_to_remove:
        section_to_remove.decompose()

    content = soup.findAll("div", class_="elementor-widget-theme-post-content")
    assert len(content) == 1, "More than one content section was found"

    content_tags = ["p", "ul", "h1", "h2", "h3", "h4", "h5", "h6"]
    filtered_tags = content[0].find_all(content_tags)

    return "\n".join([str(x) for x in filtered_tags])


def get_article_information(article):
    metadata = {"created_at": datetime.now().isoformat()}
    response = {}

    try:
        id = article.get("post_id")
        response["post_id"] = id
    except Exception as err:
        logger.error(f"[ERROR] Problem to get 'id'. {err}")

    try:
        category = article.find("a", rel="tag").text
        response["category"] = category
    except Exception as err:
        logger.error(f"[ERROR] Problem to get 'category'. {err}")

    try:
        article_thumb = [
            x.find("a")
            for x in article.findAll(
                "h2", attrs={"class": "elementor-heading-title elementor-size-default"}
            )
            if 'rel="tag"' not in str(x)
        ][0]
    except Exception as err:
        logger.error(f"[ERROR] Problem to get 'article_thumb'. {err}")

    try:
        title = article_thumb.text
        response["title"] = title
    except Exception as err:
        logger.error(f"[ERROR] Problem to get 'title'. {err}")

    try:
        author = " ".join(
            [
                element.text
                for element in partition_html(
                    text=str(
                        article.find(
                            "span", class_="elementor-post-info__item--type-author"
                        )
                    )
                )
            ]
        )
        response["author"] = author
    except Exception as err:
        logger.error(f"[ERROR] Problem to get 'author'. {err}")

    try:
        date = " ".join(
            [element.text for element in partition_html(text=str(article.find("time")))]
        )
        response["date"] = date
    except Exception as err:
        logger.error(f"[ERROR] Problem to get 'date'. {err}")

    try:
        url = article_thumb.get("href")
        response["url"] = url
    except Exception as err:
        logger.error(f"[ERROR] Problem to get 'url'. {err}")

    try:
        html_raw_content = get_html_content(url)
    except Exception as err:
        logger.error(f"[ERROR] Problem to get 'html_raw_content'. {err}")

    try:
        content = get_content(html_raw_content)
        response["content"] = content
    except Exception as err:
        logger.error(
            f"[ERROR] Problem to get 'content' in article '{response['title']}'. {err}"
        )

    try:
        id = create_hash(url)
        response["id"] = id
    except Exception as err:
        logger.error(f"[ERROR] Problem to get 'id'. {err}")

    response["metadata"] = metadata
    return response


def persist_article(
    article_repo: ArticleRepository,
    article_info: dict,
    overwrite: bool = False,
):
    try:
        article_repo.insert(**article_info)
    except IntegrityError as err:
        if overwrite:
            logger.debug(f"Updating article '{article_info['title']}'.")
            article_repo.insert_or_update(**article_info)
        else:
            if "UNIQUE constraint failed" in str(err):
                raise DuplicateArticleError(
                    f"The article '{article_info['title']}' is already present in database. Try to set `overwrite=True`"
                )
            raise err
    except Exception as err:
        logger.error(
            f"[ERROR] It was not possible to persist the article '{article_info['title']}'. {err}"
        )


def process_article(
    article_repo: ArticleRepository,
    article: bs4.element.Tag,
    overwrite: bool = False,
):
    article_info = get_article_information(article)
    persist_article(article_repo, article_info, overwrite)
