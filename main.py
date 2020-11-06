import io
import xml.etree.ElementTree as ET
from grab import Grab
from newspaper import Article


class Newspaper:
    def news(self, limit=5):
        all_news = self._get_all_news()
        return [next(all_news) for _ in range(limit)]

    @staticmethod
    def grub(url):
        article = Article(url, language='ru')
        article.download()
        article.parse()
        return {'title': article.title,
                'image': article.top_image,
                'content': article.text.split('\n\n')
                }

    def _get_all_news(self):
        g = Grab()
        resp = g.go(self.url)
        xml_file = io.StringIO(resp.unicode_body())
        xmlp = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(xml_file, parser=xmlp)
        root = tree.getroot()
        for item in root.iter('item'):
            yield {
                'title': item.find('title').text,
                'link': item.find('link').text,
                'desc': item.find('description').text,
                'published': item.find('pubDate').text
            }


class Lenta(Newspaper):
    url = 'http://lenta.ru/rss'


class Interfax(Newspaper):
    url = 'http://www.interfax.ru/rss.asp'


class Kommersant(Newspaper):
    url = 'http://www.kommersant.ru/RSS/news.xml'


class M24(Newspaper):
    url = 'http://www.m24.ru/rss.xml'


lenta = M24()
news = lenta.news(limit=2)
url = news[0]['link']

data = lenta.grub(url)
print(data)
