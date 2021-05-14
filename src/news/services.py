from news.models import Article


def get_last_news():
    return Article.objects.all()[:10]