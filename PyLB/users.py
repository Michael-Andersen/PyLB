from PyLB.getpage import get_page
import random

def get_users_by_film_per_page(film, page, order=''):
    random_orders = ['/', '/by/date-earliest/', '/by/member-rating/']
    possible_orders = {'newest': '/', 'oldest': '/by/date-earliest/', 'highest': '/by/member-rating/',
                       'lowest': '/by/member-rating-lowest/'}
    if order not in possible_orders.keys():
        order = random_orders[random.randrange(0, len(random_orders))]
    else:
        order = possible_orders[order]
    url = f'https://letterboxd.com/film/{film}/likes{order}page/{page}'
    soup = get_page(url)
    text = soup.find_all(class_='name')
    users = []
    for i in text:
        raw = str(i)
        raw = raw.replace('<a class="name" href="', '')
        raw = raw.split('"')
        users.append(raw[0].split("/")[1])
    return users

def get_users_by_film_all(film, page, order=''):
    users = []
    userset = get_users_by_film_per_page(film, 1, order)
    i = 2
    while userset:
        users.extend(userset)
        userset = get_user_likes_per_page(film, i, order)
        i += 1
    return users

def get_users_by_film(film, page=None, order=''):
    text = []
    first_time = True
    if not page:
        page = random.randint(0, 20)
        while len(text) < 25 and page != 1:
            if not first_time:
                page = page // 2
            text = get_users_by_film_per_page(film, page, order)
            first_time = False
    elif page == 'all':
        text = []
        textset = get_users_by_film_per_page(film, 1, order)
        i = 2
        while textset:
            text.extend(textset)
            textset = get_user_likes_per_page(film, i, order)
            i += 1
    user_links = []
    for i in text:
        raw = str(i)
        raw = raw.replace('<a class="name" href="', '')
        raw = raw.split('"')
        user_links.append(raw[0].split("/")[1])
    return user_links

def get_user_likes_per_page(user, page, order=''):
    url = f'https://letterboxd.com/{user}/likes/films/page/{page}'
    soup = get_page(url)
    text = soup.find_all(class_='poster')
    films = []
    for i in text:
        raw = str(i)
        raw = raw.split('data-film-slug="/film/', 2)
        raw = raw[1].split('/')
        films.append(raw[0])
    return films

def get_user_likes_all(user):
    films = []
    filmset = get_user_likes_per_page(user, 1)
    i = 2
    while filmset:
        films.extend(filmset)
        filmset = get_user_likes_per_page(user, i)
        i += 1
    return films


