from uuid import uuid4
from pytils.translit import slugify
def unique_slugify(instanse, slug):
    '''
    Генератор случайного slug в случае существования уже введенного
    '''

    model = instanse.__class__
    # Преобразование строки в slug
    unique_slug = slugify(slug)
    # Если slug существует, то генерируется новый рандомный slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}--{uuid4().hex[:8]}'
    return unique_slug