from typing import List, Optional
from pydantic import BaseModel
from bs4 import BeautifulSoup


class FeedItem(BaseModel):
    title: str
    pub_date: str
    link: str
    thumbnail: str
    description: str
    categories: str

    def __hash__(self):
        return hash(self.title.strip())

    def __eq__(self, other):
        return self.title.strip() == other.title.strip()


class RSSFeed(BaseModel):
    title: str
    version: Optional[str]
    language: Optional[str]
    description: Optional[str]
    feed: List[FeedItem]


class Parser:
    """Parser for rss files."""

    def __init__(self, xml: str):
        self.xml = xml
        self.raw_data = None
        self.rss = None

    @staticmethod
    def get_text(item: object, attribute: str) -> str:
        """
        Return the text information about an attribute of an object.
        If it is not present, it will return an empty string.
        """
        return getattr(getattr(item, attribute, ""), "text", "")

    def parse(self) -> RSSFeed:
        main_soup = BeautifulSoup(self.xml, "xml")

        self.raw_data = {
            "title": main_soup.title.text,
            "version": main_soup.rss.get("version"),
            "language": getattr(main_soup.language, "text", ""),
            "description": getattr(main_soup.description, "text", ""),
            "feed": [],
        }

        items = main_soup.findAll("item")
        for item in items:
            link = self.get_text(item, "link")
            if not link:
                link = self.get_text(item, "guid")

            enclosure = item.find("enclosure")
            if enclosure:
                image = enclosure.get("url")

            item_dict = {
                "title": self.get_text(item, "title"),
                "pub_date": self.get_text(item, "pubDate"),
                "link": link,
                "thumbnail": image,
                "description": self.get_text(item, "description"),
                "categories": self.get_text(item, "category"),
            }

            self.raw_data["feed"].append(item_dict)

        return RSSFeed(**self.raw_data)
