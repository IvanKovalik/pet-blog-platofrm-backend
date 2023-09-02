from pages.models import Article
import string
import random
from accounts.models import CustomUser


def __create_string_with_length(length):
    s = ''.join(random.choices(string.ascii_uppercase + string.digits + string.whitespace, k=length))
    return s


def choose_random_author():
    pass


def create_many_articles(number_of_articles: int):
    for i in range(number_of_articles):
        Article.objects.create(
            name=__create_string_with_length(18),
            author_id=random.randint(4, 400),
            text=__create_string_with_length(random.randint(5000, 12000)),
            views=random.randint(100, 10000)
        )
