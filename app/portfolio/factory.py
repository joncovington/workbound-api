import factory
from random import randint
from faker import Faker
from portfolio.models import Task
from core.factory import SuperUserFactory


def get_title() -> str:
    '''Returns a string containing one or two words'''
    FAKE = Faker()
    title_tuple = FAKE.words(nb=randint(1, 2))
    title = ''
    for word in title_tuple:
        title = title + f' {word}'
    title = title.lstrip()
    return title


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyFunction(get_title)
    description = factory.Faker('paragraph')
    duration = factory.Faker('pyint', min_value=0, max_value=60)
    completion_days = factory.Faker('pyint', min_value=0, max_value=10)
    created_by = factory.SubFactory(SuperUserFactory)

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        title = kwargs['title']
        print(title)
        kwargs['title'] = str(title).title()
        return kwargs
