import json
from textwrap import dedent

import pandas as pd


class PageRepository:
    def __init__(self, connection, table_name: str = "page"):
        self.connection = connection
        self.table_name = table_name
        self.connection.connect()
        self.create_table()

    def create_table(self):
        self.connection.cursor.execute(
            dedent(
                f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                html_content TEXT NOT NULL,
                metadata TEXT
            )
        """
            )
        )
        self.connection.conn.commit()

    def insert_page(self, url, html_content, metadata=None):
        # Converte o dicionário de metadata para uma string JSON
        metadata_json = json.dumps(metadata) if metadata else None
        self.connection.cursor.execute(
            dedent(
                f"""
            INSERT INTO {self.table_name} (url, html_content, metadata) VALUES (?, ?, ?)
        """
            ),
            (url, html_content, metadata_json),
        )
        self.connection.conn.commit()

    def get_all_pages(self):
        self.connection.cursor.execute(f"SELECT * FROM {self.table_name}")
        return self.connection.cursor.fetchall()


class ArticleRepository:
    def __init__(self, connection, table_name: str = "article"):
        self.connection = connection
        self.table_name = table_name
        self.connection.connect()
        self.create_table()

    def create_table(self):
        self.connection.cursor.execute(
            dedent(
                f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id TEXT PRIMARY KEY,
                post_id TEXT,
                title TEXT,
                author TEXT,
                date TEXT,
                category TEXT,
                url TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT
            )
        """
            )
        )
        self.connection.conn.commit()

    def insert(
        self, id, post_id, title, author, date, category, url, content, metadata=None
    ):

        try:
            metadata_json = json.dumps(metadata) if metadata else None
            self.connection.cursor.execute(
                dedent(
                    f"""
                INSERT INTO {self.table_name} (id, post_id, title, author, date, category, url, content, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
                ),
                (
                    id,
                    post_id,
                    title,
                    author,
                    date,
                    category,
                    url,
                    content,
                    metadata_json,
                ),
            )
            self.connection.conn.commit()
        finally:
            self.connection.cursor.close()
            self.connection.conn.close()
            self.connection.connect()

    def insert_or_update(
        self, id, post_id, title, author, date, category, url, content, metadata=None
    ):

        try:
            metadata_json = json.dumps(metadata) if metadata else None
            self.connection.cursor.execute(
                dedent(
                    f"""
                INSERT OR REPLACE INTO {self.table_name} (id, post_id, title, author, date, category, url, content, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
                ),
                (
                    id,
                    post_id,
                    title,
                    author,
                    date,
                    category,
                    url,
                    content,
                    metadata_json,
                ),
            )
            self.connection.conn.commit()
        finally:
            self.connection.cursor.close()
            self.connection.conn.close()
            self.connection.connect()

    def get_column_names(self):
        self.connection.cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns = [info[1] for info in self.connection.cursor.fetchall()]
        return columns

    def get_all(self):
        columns = self.get_column_names()
        self.connection.cursor.execute(f"SELECT * FROM {self.table_name}")
        articles = self.connection.cursor.fetchall()
        return pd.DataFrame(articles, columns=columns)
