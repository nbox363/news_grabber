import io
import xml.etree.ElementTree as ET
from grab import Grab
from newspaper import Article
from typing import Generator
from xml.etree.ElementTree import Element


class NewsSite:
    def news(self, limit=5) -> list:
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
        xml_root = self._get_xml_root()
        for item in xml_root.iter('item'):
            yield {
                'title': item.find('title').text,
                'link': item.find('link').text,
                'desc': item.find('description').text,
                'published': item.find('pubDate').text
            }

    def _get_xml_root(self) -> Element:
        g = Grab()
        resp = g.go(self.url)
        xml_file_obj = io.StringIO(resp.unicode_body())
        xml_parser = ET.XMLParser(encoding="utf-8")
        xml_tree = ET.parse(xml_file_obj, parser=xml_parser)
        xml_root = xml_tree.getroot()
        return xml_root


class Lenta(NewsSite):
    url = 'http://lenta.ru/rss'


class Interfax(NewsSite):
    url = 'http://www.interfax.ru/rss.asp'


class Kommersant(NewsSite):
    url = 'http://www.kommersant.ru/RSS/news.xml'


class M24(NewsSite):
    url = 'http://www.m24.ru/rss.xml'
