from grabber import Lenta, Interfax, Kommersant, M24


lenta = Lenta()
news = lenta.news(limit=2)
url = news[0]['link']
data = lenta.grub(url)


interfax = Interfax()
news = interfax.news(limit=2)
url = news[0]['link']
data = interfax.grub(url)


komersant = Kommersant()
news = komersant.news(limit=2)
url = news[0]['link']
data = komersant.grub(url)


m24 = M24()
news = m24.news(limit=2)
url = news[0]['link']
data = m24.grub(url)
