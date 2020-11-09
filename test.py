import requests
import unittest
from grabber import NewsGrabber
from unittest.mock import patch

xml_example = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <language>ru</language>
    <title>Lenta.ru : Новости</title>
    <description>Новости, статьи, фотографии, видео. Семь дней в неделю, 24 часа в сутки.</description>
    <link>https://lenta.ru</link>
    <image>
      <url>https://lenta.ru/images/small_logo.png</url>
      <title>Lenta.ru</title>
      <link>https://lenta.ru</link>
      <width>134</width>
      <height>22</height>
    </image>
    <atom:link rel="self" type="application/rss+xml" href="http://lenta.ru/rss"/>
    <item>
        <guid>https://lenta.ru/news/2020/11/05/volni/</guid>
        <title>Title</title>
        <link>https://google.com</link>
        <description>
            <![CDATA[Description.]]>
        </description>
        <pubDate>Thu, 05 Nov 2020 20:19:19 +0300</pubDate>
        <enclosure url="https://icdn.lenta.ru/images/2020/11/05/16/20201105165224119/pic_ea82bc4ff2b8d6e52b7f332c0943b138.jpg" type="image/jpeg" length="68676"/>
        <category>Путешествия</category>
    </item>
  </channel>
</rss>'''

expected_output = [{
    'title': 'Title',
    'link': 'https://google.com',
    'desc': 'Description.',
    'published': '2020.11.05 20:19'
}]

class News(NewsGrabber):
    # this methid implemented to satisfy NewsGrabber interface but not used in test due to mock
    def get_url(self) -> str:
        return ''


def my_requests_get(_url):
    class FakeResp:
        text = xml_example

    return FakeResp()


class TestNewsSite(unittest.TestCase):

    def setUp(self) -> None:
        self.news = News()

    @patch.object(requests, 'get', side_effect=my_requests_get)
    def test_news(self, _mocked_requests):
        self.assertEqual(self.news.news(),
                         expected_output, 'incorrect output')


if __name__ == '__main__':
    unittest.main()
