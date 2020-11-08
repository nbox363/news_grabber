import io
import requests
import xml.etree.ElementTree as ET

from abc import ABC, abstractmethod
from newspaper import Article
from typing import Generator
from xml.etree.ElementTree import Element


class NewsGrabber(ABC):
    @abstractmethod
    def get_url() -> str:
        raise NotImplementedError

    def news(self, limit=1) -> list:
        news = self._get_news()
        return [next(news) for _ in range(limit)]

    @staticmethod
    def grub(url) -> dict:
        article = Article(url, language='ru')
        article.download()
        article.parse()
        return {'title': article.title,
                'image': article.top_image,
                'content': article.text.split('\n\n')
                }

    def _get_news(self) -> Generator[dict, None, None]:
        """Walks through xml tree and yields dict for every item node"""
        xml_root = self._get_xml_root()
        for item in xml_root.iter('item'):
            yield {
                'title': item.find('title').text,
                'link': item.find('link').text,
                'desc': item.find('description').text.strip(),
                'published': item.find('pubDate').text
            }

    def _get_xml_root(self) -> Element:
        """Goes to the internet for xml and return xml root"""
        resp = requests.get(self.get_url())
        xml_file_obj = io.StringIO(resp.text)
        xml_parser = ET.XMLParser(encoding="utf-8")
        xml_tree = ET.parse(xml_file_obj, parser=xml_parser)
        xml_root = xml_tree.getroot()
        return xml_root


class Lenta(NewsGrabber):
    def get_url(self):
        return 'http://lenta.ru/rss'


class Interfax(NewsGrabber):
    def get_url(self):
        return 'http://www.interfax.ru/rss.asp'


class Kommersant(NewsGrabber):
    def get_url(self):
        return 'http://www.kommersant.ru/RSS/news.xml'


class M24(NewsGrabber):
    def get_url(self):
        return 'http://www.m24.ru/rss.xml'


lenta = Lenta()
news = lenta.news(limit=2)
